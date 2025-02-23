import os
import json
import xml.etree.ElementTree as ET

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

    save_directory = "./pages/kasra/"
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

            for page in sub_book.findall("page"):
                page_persian = page.get("navtitle", sub_persian)  # Use parent name if not found
                page_english = convert_persian_to_english(page_persian)

                page_path = os.path.join(sub_path, page_english)
                create_folder_with_meta_json(sub_path, page_english, page_persian)

if __name__ == "__main__":
    xml_file_path = "KasraHelp.toc.txt"
    save_directory = "./pages"
    print(f"📂 Saving to: {save_directory}")
    process_xml(xml_file_path, save_directory)





