import os
import json
import xml.etree.ElementTree as ET
import shutil
import requests
import html2text
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urlparse, unquote
import re
import time


BASE_URL = "https://kasrayar.depna.com"  # پایه آدرس برای دانلود صفحات HTML

# Get the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

save_directory = os.path.join(BASE_DIR, "pages")
static_img_dir = os.path.join(BASE_DIR, "public", "img")
static_assets_dir = os.path.join(BASE_DIR, "public", "assets")

index_file_path = os.path.join(save_directory, 'index.mdx')
max_pages=500


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

def save_content(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 Saved: {os.path.relpath(path)}")

def crawl_website(start_urls, save_directory, page_title):
    urls_queue = deque([start_urls])  # Initialize the queue with the start URL
    visited_urls = set()
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    asset_extensions = ['.zip', '.pdf', '.docx', '.xlsx', '.pptx']
    all_links = []

    print(f"Starting crawl with {len(urls_queue)} URLs in the queue.")
    print(f"Base domain: {BASE_URL}")

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

            print(f"Added {current_url} to visited URLs.")

            # Add to index
            relative_path = os.path.relpath(md_path, start=save_directory).replace('\\', '/')
            link_text = os.path.splitext(os.path.basename(md_path))[0]
            all_links.append(f'<li><a href="/docs/{relative_path}">{link_text}</a></li>')

            # Extract new links
            new_urls = extract_links(soup, current_url, BASE_URL)
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
    # create_index_page(all_links, index_file_path)


def has_persian(text):
    # الگوی یونیکد برای حروف فارسی (پایۀ بازۀ 0600 تا 06FF)
    persian_pattern = re.compile('[\u0600-\u06FF]')
    return bool(persian_pattern.search(text))


def copy_image_to_new_folder(img_file_path):
    # مسیر را نرمال کنیم
    img_file_path = os.path.normpath(img_file_path)
    # درایو (مثلاً D:) و بقیه مسیر را جدا کنیم
    drive, tail = os.path.splitdrive(img_file_path)
    # حالا اگر مثلاً drive = 'D:', tail = '\saberprojects\...'
    # پوشه‌ها را از قسمت tail جدا می‌کنیم
    parts = tail.split(os.sep)  # ['', 'saberprojects', 'kasra', ...]
    # آخرین بخش parts نام فایل است
    filename = parts[-1]
    # مابقی، پوشه‌های مسیر هستند
    folders = parts[:-1]
    # اگر اولین پوشه خالی بود (مثلاً به‌خاطر اسلش اول)، آن را حذف می‌کنیم
    # چراکه split('\saberprojects\...') ممکن است با یک '' شروع شود
    if folders and folders[0] == '':
        folders = folders[1:]
    # روی فولدرها حلقه می‌زنیم؛ اگر حروف فارسی داشتند، تبدیلشان می‌کنیم
    for i in range(len(folders)):
        if has_persian(folders[i]):
            folders[i] = convert_persian_to_english(folders[i])

    # جدا کردن نام فایل و پسوند
    name, ext = os.path.splitext(filename)
    # تبدیل پسوند به حروف کوچک
    ext = ext.lower()
    # ساخت نام جدید فایل
    new_filename = name + ext

    # حالا با هم دوباره یک مسیر صحیح می‌سازیم
    # برای ساخت مسیر کامل درایو را با اسلش اضافه می‌کنیم
    # به جای drive='D:' → 'D:\' یا 'D:/' (در ویندوز فرقی نمی‌کند)
    new_dir = os.path.join(drive + os.sep, *folders)
    new_path = os.path.join(new_dir, new_filename)

    # ساختن فولدر اگر وجود ندارد
    os.makedirs(new_dir, exist_ok=True)
    # کپی فایل
    shutil.copy(img_file_path, new_path)
    # حذف پوشه و تصویر قدیمی پس از کپی
    if os.path.exists(img_file_path):
        os.remove(img_file_path)  # حذف تصویر قدیمی
        
    if os.path.exists(new_dir) and not os.listdir(new_dir):
        os.rmdir(new_dir)  # حذف پوشه اگر خالی باشد

    print("😴Old path:", img_file_path)
    print("😍New path:", new_path)
    return new_path


def extract_links(soup, base_url, base_domain):
    links = []
    for tag in soup.find_all(['a', 'link'], href=True):
        href = tag['href']
        absolute_url = urljoin(base_url, href)
        if urlparse(absolute_url).netloc == base_domain:
            links.append(absolute_url)
    return links


def is_not_english(text):
    """Check if the given text is not in English (i.e., contains non-ASCII characters)."""
    return any(ord(char) >= 128 for char in text)


def get_first_title_from_mdx(md_content):
    """Extracts the first title from the given markdown content (first H1 tag)."""
    lines = md_content.splitlines()
    for line in lines:
        line = line.strip()  # Clean up extra spaces
        if line.startswith('# '):  # Assuming the title is the first H1
            return line[2:].strip()  # Return the title without the '# ' and any extra spaces
    return None  # Return None if no title is found


def escape_special_characters(md_content):
    """Escapes problematic characters for MDX compatibility."""
    # Replace special characters
    md_content = md_content.replace('<<', '&#60;&#60;').replace('>>', '&#62;&#62;')
    md_content = md_content.replace('<', '&#60;').replace('>', '&#62;')
    md_content = md_content.replace('​', '')  # Remove U+200E character (zero-width non-joiner)
    md_content = md_content.replace('‏', '')  # Remove 
    md_content = md_content.replace('[U+200E]', '')
    return md_content


def add_front_matter(md_path, md_content, original_title=None):
    """Adds front matter with support for Persian titles."""
    base_name = os.path.splitext(os.path.basename(md_path))[0]

    # Attempt to extract title from first H1 tag
    title = original_title or base_name
    extracted_title = get_first_title_from_mdx(md_content)

    # If title is found in the content, use it
    if extracted_title:
        title = extracted_title
    formatted_content = replace_strange_characters(md_content)
    # Escape special characters in the MDX content
    formatted_content = escape_special_characters(formatted_content)

    # Create front matter with extracted title
    front_matter = f"""---
id: "{base_name}"
title: "{title}"
---

"""
    # Combine front matter and original markdown content
    final_content = front_matter + formatted_content

    # Save the updated content to the file
    save_content(md_path, final_content)

def replace_strange_characters(md_content):
    formatted_content = ""
    inside_json = False
    for line in md_content.split('\n'):
        line = line.replace('\\', '/')  # Replace backslashes with forward slashes
        line = re.sub(r'/{2,}', '/', line)  # Remove repeated slashes
        if '<Path>' in line and not inside_json:
            formatted_content = line.replace('<Pa', '[Pa').replace('th>', 'th]') + "\n"
        elif '<user>' in line and not inside_json:
            formatted_content = line.replace('<us', '[us').replace('er>', 'er]') + "\n"
        elif '{' in line and not inside_json:
            formatted_content += "```json\n" + line + "\n"
            inside_json = True
        elif '}' == line:
            formatted_content += line + "\n" + "```\n"
            inside_json = False
        else:
            formatted_content += line + "\n"
    return formatted_content

def create_file_path(url, base_dir, extension):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = re.sub(r'\.html?$', '', path)  # حذف پسوند .htm/.html
    path_parts = unquote(path.strip('/')).split('/')
    file_name = convert_persian_to_english(os.path.basename(path_parts[-1])) + extension
    # فقط نام فایل را برمی‌گردانیم
    return os.path.join(base_dir, file_name)

def create_index_page(new_links, index_file_path):
    try:
        # Read the existing content if the file exists
        with open(index_file_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        # Extract existing links if any
        start = existing_content.find('<ul>') + 4
        end = existing_content.find('</ul>')
        existing_links = existing_content[start:end].strip().split('\n') if start != 3 and end != -1 else []
    except FileNotFoundError:
        existing_links = []
    # Combine the existing links with the new links
    combined_links = existing_links + new_links
    # Create the new index content
    index_content = """
# فهرست

## صفحات

<ul>
    {links}
</ul>
""".format(links='\n    '.join(combined_links))
    
    with open(index_file_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"📄 Index page created: {index_file_path}")


def download_and_save_media(soup, base_url, static_img_dir, static_assets_dir):
    # Handle images
    for img_tag in soup.find_all('img', src=True):
        img_url = img_tag['src']
        img_full_url = urljoin(base_url, img_url)
        img_file_path = save_media_file(img_full_url, static_img_dir)
        if(is_not_english(img_file_path)): # used
            img_file_path = copy_image_to_new_folder(img_file_path)
        # img_file_path = copy_image_to_new_folder(img_file_path)
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
            # asset_file_path = copy_image_to_new_folder(asset_file_path)
            if asset_file_path:
                # Update href to '/assets/...'
                asset_relative_path = '/assets/' + os.path.relpath(asset_file_path, static_assets_dir).replace('\\', '/')
                a_tag['href'] = asset_relative_path

def is_media_url(url, extensions =[]):
    return any(url.lower().endswith(ext) for ext in extensions)

def save_media_file(url, save_dir):
    try:
        parsed_url = urlparse(url)
        media_path = os.path.join(save_dir, unquote(parsed_url.path.lstrip('/')))
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        os.makedirs(os.path.dirname(media_path), exist_ok=True)
        with open(media_path, 'wb') as file:
            file.write(response.content)

        # Rename the file if it has a .PNG extension
        if media_path.lower().endswith('.png'):
            new_media_path = media_path[:-4] + '.png'
            os.rename(media_path, new_media_path)
            print(f"📦 Media saved and renamed: {os.path.relpath(new_media_path)}")
            return new_media_path
        else:
            print(f"📦 Media saved: {os.path.relpath(media_path)}")
            return media_path



    except Exception as e:
        print(f"❌ Error downloading media {url}: {str(e)}")
        return None
    

def convert_to_markdown(soup):
    """تبدیل HTML به Markdown و حفظ کاراکترهای یونیکد و مدیریت کدبلاک‌های JSON"""
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    # مدیریت کدبلاک‌های JSON
    for script in soup.find_all('script', type='application/json'):
        json_content = json.loads(script.string)
        json_code_block = f"```json\n{json.dumps(json_content, indent=4)}\n```"
        script.replace_with(json_code_block)  # Replace JSON script with markdown code block
    markdown_content = converter.handle(str(soup))
    return markdown_content.encode('utf-8').decode('utf-8')



def rename_png_files_in_subdirectories(directory):
    # Walk through all directories and files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file has a .PNG extension
            if filename.endswith('.PNG'):
                # Create the new filename with .png extension
                new_filename = filename[:-4] + '.png'
                # Get the full path of the old and new filenames
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} to {new_file_path}')



def convert_persian_to_english(persian_name):
    """Converts Persian characters to their English equivalents for folder naming."""
    translation_map = {
        'آ': 'aa','ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 
        'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 
        'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 
        'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v', 
        'ه': 'h', 'ی': 'y', ' ': '_', ':': '_', '/': '_', '-': '_',
         '.': '_', 'ء': 'e' , 'ئ': 'y', ' ': '-', '،': '-', '(': '-', ')': '-'
    }

    # Replace Zero Width Non-Joiner (U+200C) and Left-to-Right Mark (U+200E) with '_'
    persian_name = persian_name.replace('\u200C', '_')  # U+200C: Zero Width Non-Joiner
    persian_name = persian_name.replace('\u200E', '_')  # U+200E: Left-to-Right Mark
    return ''.join(translation_map.get(char, char) for char in persian_name)


def create_folder_with_meta_json(base_dir, english_name, persian_name):
    """Creates a folder and updates the _meta.json file."""
    folder_path = os.path.join(base_dir, english_name)
    os.makedirs(folder_path, exist_ok=True)
    
    meta_file_path = os.path.join(base_dir, '_meta.json')
    meta_data = {}

    if os.path.exists(meta_file_path):
        with open(meta_file_path, 'r', encoding='utf-8') as meta_file:
            meta_data = json.load(meta_file)

    meta_data[english_name] = persian_name

    with open(meta_file_path, 'w', encoding='utf-8') as meta_file:
        json.dump(meta_data, meta_file, ensure_ascii=False, indent=4)
    
    print(f"📂 Created folder: {folder_path}")
    print(f"📄 Updated _meta.json: {meta_file_path}")
    return folder_path  # مسیر پوشه برگشت داده شود

def download_and_convert_html(page_href, save_directory, page_title):
    page_href = page_href.replace("../contents", "")
    """Downloads HTML page, converts to Markdown, and saves as .mdx"""
    full_url = f"{BASE_URL}/{page_href.lstrip('../')}"  # اطمینان از مسیر صحیح

    crawl_website(full_url,save_directory, page_title)


def process_book_or_page(element, parent_directory):
    """Recursively processes books and pages, creating folders and downloading content."""
    if element.tag == "book":
        persian_name = element.get("navtitle")
        if not persian_name:
            href = element.get("href")
            persian_name = os.path.splitext(os.path.basename(href))[0]

        english_name = convert_persian_to_english(persian_name)
        # Create folder for this book
        book_path = create_folder_with_meta_json(parent_directory, english_name, persian_name)

        # Process children (sub-books and pages)
        for child in element:
            process_book_or_page(child, book_path)

    elif element.tag == "page":
        page_title = element.get("navtitle", "")
        page_href = element.get("href")

        if page_href:
            download_and_convert_html(page_href, parent_directory, page_title)
    else:
        return ""

def process_xml(xml_file, save_directory):
    """Parses the XML TOC file and processes all books and pages."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for book in root.findall("book"):
        persian_name = book.get("navtitle")
        if persian_name == "نسل یک":  # Skipping this section
            continue
        process_book_or_page(book, save_directory)

def remove_main_folder_and_contents(save_directory):
    """Deletes and recreates the main folder for fresh processing."""
    remove_all_recursive(save_directory)    
    assets_directory = "./public/img/"
    remove_all_recursive(assets_directory)

def remove_all_recursive(save_directory):
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)
    os.makedirs(save_directory)
    print(f"📂 Cleared and recreated: {save_directory}")

if __name__ == "__main__":
    xml_file_path = "KasraHelp.toc.txt"
    save_directory = "./pages"
    print(f"📂 Saving to: {save_directory}")
    remove_main_folder_and_contents(save_directory+'/kasra')

    process_xml(xml_file_path, save_directory)

