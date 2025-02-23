import os
import json
import xml.etree.ElementTree as ET
import shutil
import requests
import html2text
from bs4 import BeautifulSoup



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

def convert_to_markdown(soup):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    return converter.handle(str(soup))

def convert_persian_to_english(persian_name):
    """Converts Persian characters to their English equivalents for folder naming."""
    translation_map = {
        'آ': 'aa','ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 
        'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 
        'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 
        'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v', 
        'ه': 'h', 'ی': 'y', ' ': '_', ':': '_', '/': '_', '-': '_', '.': '_'
    }
    return ''.join(translation_map.get(char, char) for char in persian_name)

def create_folder_with_meta_json(base_dir, english_name, persian_name):
    """Creates a folder and updates the _meta.json file."""
    folder_path = os.path.join(base_dir, english_name)
    os.makedirs(folder_path, exist_ok=True)
    
    meta_file_path = os.path.join(base_dir, '_meta.json')
    if os.path.exists(meta_file_path):
        with open(meta_file_path, 'r', encoding='utf-8') as meta_file:
            meta_data = json.load(meta_file)
    else:
        meta_data = {}

    meta_data[english_name] = persian_name

    with open(meta_file_path, 'w', encoding='utf-8') as meta_file:
        json.dump(meta_data, meta_file, ensure_ascii=False, indent=4)
    
    print(f"📂 Created folder: {folder_path}")
    print(f"📄 Updated _meta.json: {meta_file_path}")

def process_xml(xml_file, save_directory):
    """Parses the XML TOC file and creates corresponding folders."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for book in root.findall("book"):
        persian_name = book.get("navtitle")
        if persian_name == "نسل یک":
            continue
        english_name = convert_persian_to_english(persian_name)

        book_path = os.path.join(save_directory, english_name)
        create_folder_with_meta_json(save_directory, english_name, persian_name)

        for sub_book in book.findall("book"):
            sub_persian = sub_book.get("navtitle")
            sub_english = convert_persian_to_english(sub_persian)

            sub_path = os.path.join(book_path, sub_english)
            create_folder_with_meta_json(book_path, sub_english, sub_persian)

            for sub_book in book.findall("book"):
                sub_persian = sub_book.get("navtitle")
                sub_english = convert_persian_to_english(sub_persian)
                sub_path = os.path.join(book_path, sub_english)
                create_folder_with_meta_json(book_path, sub_english, sub_persian)

            for page in sub_book.findall("page"):
                page_href = page.get("href")
                if page_href:
                    # Download the HTML file
                    html_url = f"https://kasrayar.depna.com{page_href}"
                    response = requests.get(html_url)
                    response.raise_for_status()

                    # Create the file path for saving
                    page_english_name = convert_persian_to_english(persian_name) + ".htm"
                    html_file_path = os.path.join(book_path, page_english_name)

                    # Save the HTML file
                    with open(html_file_path, 'wb') as html_file:
                        html_file.write(response.content)
                    print(f"📄 Downloaded HTML file: {html_file_path}")

                    # Convert HTML to Markdown
                    md_content = convert_to_markdown(BeautifulSoup(response.text, 'html.parser'))
                    md_file_path = os.path.splitext(html_file_path)[0] + ".md"
                    save_content(md_file_path, md_content)

                    # Update the _meta.json file
                    update_meta_json(book_path, persian_name, page_english_name)

def remove_main_folder_and_contents():
    save_directory = "./pages/kasra/"

    # پاک کردن محتویات پوشه
    if os.path.exists(save_directory):
        shutil.rmtree(save_directory)
        os.makedirs(save_directory)
        print(f"📂 پوشه '{save_directory}' پاک شد و دوباره ایجاد گردید.")
    return save_directory

if __name__ == "__main__":
    xml_file_path = "KasraHelp.toc.txt"
    save_directory = "./pages"
    print(f"📂 Saving to: {save_directory}")
    save_directory = remove_main_folder_and_contents()

    process_xml(xml_file_path, save_directory)





