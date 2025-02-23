import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# A set to keep track of URLs we’ve already visited
visited = set()

def is_markdown(url):
    return url.endswith('.md') or url.endswith('.mdx')

def save_file(url, content, output_dir):
    # Remove any query parameters
    filename = os.path.basename(url.split('?')[0])
    if not filename:
        filename = "index.html"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved:", filepath)

def crawl(url, base_url, output_dir, depth=0, max_depth=3):
    if depth > max_depth:
        return
    if url in visited:
        return

    print("Crawling:", url)
    visited.add(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("Error fetching", url, ":", e)
        return

    # If the URL itself is a markdown file, save its content
    if is_markdown(url):
        save_file(url, response.text, output_dir)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all anchor tags with an href attribute
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        # Only consider URLs that start with the base URL
        if not full_url.startswith(base_url):
            continue
        if full_url in visited:
            continue

        if is_markdown(full_url):
            try:
                file_resp = requests.get(full_url)
                file_resp.raise_for_status()
                save_file(full_url, file_resp.text, output_dir)
            except Exception as e:
                print("Error downloading file", full_url, ":", e)
        else:
            # Recursively crawl non-markdown pages (up to max_depth)
            crawl(full_url, base_url, output_dir, depth + 1, max_depth)

if __name__ == '__main__':
    # Base URL to start crawling
    base = "https://nextra.site/docs"
    # Directory where markdown files will be saved
    output_directory = "downloaded_md_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Optionally allow a max_depth parameter from the command line (default is 3)
    max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    crawl(base, base, output_directory, depth=0, max_depth=max_depth)
