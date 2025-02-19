import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from collections import deque
import html2text
import re
import json

def read_links_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        links = [line.strip() for line in file if line.strip()]
    print(f"Read {len(links)} links from {file_path}")
    return links

def crawl_website(start_urls, save_directory, static_img_dir, static_assets_dir, index_file_path, max_pages=5000):
    urls_queue = deque(start_urls)
    visited_urls = set()
    base_domain = urlparse(start_urls[0]).netloc
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    asset_extensions = ['.zip', '.pdf', '.docx', '.xlsx', '.pptx']
    all_links = []

    print(f"Starting crawl with {len(urls_queue)} URLs in the queue.")
    print(f"Base domain: {base_domain}")

    while urls_queue and len(visited_urls) < max_pages:
        current_url = urls_queue.popleft()

        if current_url in visited_urls:
            print(f"Skipping already visited URL: {current_url}")
            continue

        print(f"🔍 Processing: {current_url}")

        try:
            response = requests.get(current_url, timeout=20)
            response.encoding = 'utf-8'
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Download and save images and assets
            download_and_save_media(soup, current_url, static_img_dir, static_assets_dir)

            # Convert to Markdown
            # Remove duplicate text in dropspots
            for dropspot in soup.find_all('a', class_='dropspot'):
                open_text = dropspot.find('span', {'data-open-text': 'true'})
                close_text = dropspot.find('span', {'data-close-text': 'true'})
                if open_text and close_text and open_text.text == close_text.text:
                    open_text.decompose()
            
            md_content = convert_to_markdown(soup)
            md_path = create_file_path(current_url, save_directory, '.mdx')
            add_front_matter(md_path, md_content)

            visited_urls.add(current_url)
            print(f"Added {current_url} to visited URLs.")

            # Add to index
            relative_path = os.path.relpath(md_path, start=save_directory).replace('\\', '/')
            link_text = os.path.splitext(os.path.basename(md_path))[0]
            all_links.append(f'<li><a href="/docs/{relative_path}">{link_text}</a></li>')

            # Extract new links
            new_urls = extract_links(soup, current_url, base_domain)
            print(f"Found {len(new_urls)} new URLs on the page.")

            for url in new_urls:
                if url not in visited_urls and url not in urls_queue and not is_media_url(url, image_extensions):
                    if '/css/' in url.lower() or url.lower().endswith('.css'):
                        continue
                    urls_queue.append(url)
                    print(f"Added URL to queue: {url}")

            # Delete original HTML file if it exists
            html_path = create_file_path(current_url, save_directory, '.html')
            if os.path.exists(html_path):
                os.remove(html_path)

            time.sleep(1)

        except Exception as e:
            print(f"❌ Error processing {current_url}: {str(e)}")

    print(f"✅ Crawling finished. {len(visited_urls)} pages processed.")

    # Create the index file
    create_index_page(all_links, index_file_path)

def extract_links(soup, base_url, base_domain):
    links = []
    for tag in soup.find_all(['a', 'link'], href=True):
        href = tag['href']
        absolute_url = urljoin(base_url, href)
        if urlparse(absolute_url).netloc == base_domain:
            links.append(absolute_url)
    return links

def is_media_url(url, extensions =[]):
    return any(url.lower().endswith(ext) for ext in extensions)

def persian_to_english(text):
    """تبدیل متن فارسی به انگلیسی با استفاده از یک الگوریتم پایدار"""
    mapping = {
        'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's',
        'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z',
        'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's',
        'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f',
        'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n',
        'و': 'v', 'ه': 'h', 'ی': 'y', 'ئ': 'y', ' ': '-'
    }
    result = ''
    for char in text:
        result += mapping.get(char, char)
    return result.lower().strip('-')

def update_meta_json(directory, fa_name, en_name):
    """به‌روزرسانی یا ایجاد فایل _meta.json"""
    meta_path = os.path.join(directory, '_meta.json')
    meta_data = {}
    
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta_data = json.load(f)
    
    meta_data[en_name] = fa_name
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, ensure_ascii=False, indent=2)

def create_file_path(url, base_dir, extension):
    """ایجاد مسیر فایل با پشتیبانی از نام‌های فارسی"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = re.sub(r'\.html?$', '', path)  # حذف پسوند .htm/.html
    path_parts = unquote(path.strip('/')).split('/')
    
    # تبدیل هر بخش مسیر به انگلیسی
    en_parts = []
    current_dir = base_dir
    
    for part in path_parts:
        if any(ord(c) > 127 for c in part):  # بررسی وجود کاراکتر فارسی
            en_name = persian_to_english(part)
            en_parts.append(en_name)
            
            # ایجاد یا به‌روزرسانی _meta.json
            current_dir = os.path.join(base_dir, *en_parts[:-1])
            os.makedirs(current_dir, exist_ok=True)
            update_meta_json(current_dir, part, en_name)
        else:
            en_parts.append(part)
    
    return os.path.join(base_dir, *en_parts) + extension

def save_content(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved: {os.path.relpath(path)}")

def convert_to_markdown(soup):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    return converter.handle(str(soup))

def download_and_save_media(soup, base_url, static_img_dir, static_assets_dir):
    # Handle images
    for img_tag in soup.find_all('img', src=True):
        img_url = img_tag['src']
        img_full_url = urljoin(base_url, img_url)
        img_file_path = save_media_file(img_full_url, static_img_dir)

        if img_file_path:
            # Update img tag src to '/img/...' path
            img_relative_path = '/img/' + os.path.relpath(img_file_path, static_img_dir).replace('\\', '/')
            img_tag['src'] = img_relative_path

    # Handle other assets (e.g., zip files)
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if is_media_url(href):
            asset_full_url = urljoin(base_url, href)
            asset_file_path = save_media_file(asset_full_url, static_assets_dir)

            if asset_file_path:
                # Update href to '/assets/...'
                asset_relative_path = '/assets/' + os.path.relpath(asset_file_path, static_assets_dir).replace('\\', '/')
                a_tag['href'] = asset_relative_path

def save_media_file(url, save_dir):
    try:
        parsed_url = urlparse(url)
        media_path = os.path.join(save_dir, unquote(parsed_url.path.lstrip('/')))

        response = requests.get(url, timeout=20)
        response.raise_for_status()
        os.makedirs(os.path.dirname(media_path), exist_ok=True)
        with open(media_path, 'wb') as file:
            file.write(response.content)
        print(f"📦 Media saved: {os.path.relpath(media_path)}")

        return media_path
    except Exception as e:
        print(f"❌ Error downloading media {url}: {str(e)}")
        return None

def create_index_page(links, index_file_path):
    index_content = """
# فهرست

## صفحات

<ul>
    {links}
</ul>
""".format(links='\n    '.join(links))
    
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"📄 Index page created: {index_file_path}")

def add_front_matter(md_path, md_content, original_title=None):
    """اضافه کردن front matter با پشتیبانی از عنوان‌های فارسی"""
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    
    # استفاده از عنوان اصلی فارسی اگر موجود باشد
    title = original_title or base_name
    
    front_matter = f"""---
id: "{base_name}"
title: "{title}"
---

"""
    final_content = front_matter + md_content
    save_content(md_path, final_content)

if __name__ == "__main__":
    # Read links from the text file
    links_file_path = r"D:\saberprojects\kasra\my-website\extracted_links.txt"
    links_from_file = read_links_from_file(links_file_path)

    # Set the save directory and static directories
    save_directory = r"D:\saberprojects\kasra\kasra-docs\pages"
    static_img_dir = r"D:\saberprojects\kasra\kasra-docs\public\img"
    static_assets_dir = r"D:\saberprojects\kasra\kasra-docs\public\assets"
    # Path for the index file
    index_file_path = os.path.join(save_directory, 'index.mdx')

    # Start crawling
    start_urls = [
        "https://kasrayar.depna.com/KasraDesign_Core/Definitions/Definitions.htm",
    ] + links_from_file

    print(f"🔗 Number of links read from the file: {len(links_from_file)}")

    # Display the number of links and request user confirmation
    print("\n" + "="*50)
    print(f"🔍 Total number of found links: {len(start_urls)}")
    print("="*50)
    
    user_input = input("\n❓ Do you want to start crawling? (yes/no): ").strip().lower()
    
    if user_input != 'yes':
        print("❌ Crawling operation canceled.")
        sys.exit()
        
    print("\n✅ Starting crawling operation...")

    crawl_website(start_urls, save_directory, static_img_dir, static_assets_dir, index_file_path)
