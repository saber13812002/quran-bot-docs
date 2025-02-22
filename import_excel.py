import pandas as pd
import os
import requests
from urllib.parse import urljoin
import json

def convert_persian_to_english(persian_name):
    translation_map = {
        'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's', 'ج': 'j', 
        'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z', 'ر': 'r', 
        'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'z', 
        'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'gh', 
        'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n', 'و': 'v', 
        'ه': 'h', 'ی': 'y', ' ': '_', ':': '_', '/': '_', '\n': '_', 
        '\t': '_', '-': '_', '.': '_', ',': '_', '?': '_', '!': '_', 
        '؛': '_', '؟': '_', '(': '_', ')': '_', '{': '_', '}': '_', 
        '[': '_', ']': '_', '<': '_', '>': '_', 'ـ': '_'
    }
    return ''.join(translation_map.get(char, char) for char in persian_name)


def read_excel_data(file_path):
    # خواندن داده‌ها از فایل اکسل
    xls = pd.ExcelFile(file_path)
    
    # خواندن هر شیت به صورت دیکشنری
    sheets_data = {}
    for sheet_name in xls.sheet_names:
        sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
    
    return sheets_data

def print_data(data):
    for sheet, df in data.items():
        print(f"داده‌های شیت {sheet}:")
        print(df.head(300)) 


def create_folder_with_meta_json(save_directory, english_name, persian_name):
    base_folder = os.path.join(save_directory, english_name)

    print(base_folder)
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
        print(f"📁 پوشه '{base_folder}' ایجاد شد.")
    else:
        print(f"📁 پوشه '{base_folder}' قبلاً وجود دارد.")


    meta_file_path = os.path.join(save_directory, '_meta.json')

    if os.path.exists(meta_file_path):
        with open(meta_file_path, 'r', encoding='utf-8') as meta_file:
            existing_meta_content = json.load(meta_file)
        
        existing_meta_content[english_name] = persian_name
        
        with open(meta_file_path, 'w', encoding='utf-8') as meta_file:
            json.dump(existing_meta_content, meta_file, ensure_ascii=False, indent=4)
        print(f"📄 اطلاعات جدید به فایل '_meta.json' اضافه شد: {meta_file_path}")

    else:
        # اگر فایل '_meta.json' وجود ندارد، یک دیکشنری جدید ایجاد کنید
        new_meta_content = {english_name: persian_name}
        with open(meta_file_path, 'w', encoding='utf-8') as meta_file:
            json.dump(new_meta_content, meta_file, ensure_ascii=False, indent=4)
        print(f"📄 فایل '_meta.json' جدید ایجاد شد: {meta_file_path}")


# main

if __name__ == "__main__":
    file_path = 'Table Of Contents.report_.xlsx'
    data = read_excel_data(file_path)
    # print_data(data)

    save_directory = r"D:\saberprojects\kasra\kasra-docs\pages"
    static_img_dir = r"D:\saberprojects\kasra\kasra-docs\public\img"
    static_assets_dir = r"D:\saberprojects\kasra\kasra-docs\public\assets"
    # ایجاد پوشه کسرا در دایرکتوری ذخیره
    # بررسی وجود پوشه کسرا
    name_english = "kasra"
    name_persian= "کسرا";
    create_folder_with_meta_json(save_directory,name_english,name_persian)

    # save_directory_v1 = os.path.join(save_directory, 'kasra')
    # name_english_v1 = "v1"
    # name_persian_v1 = "نسل یک ";
    # create_folder_with_meta_json(save_directory_v1,name_english_v1,name_persian_v1)

    save_directory_v2 = os.path.join(save_directory, 'kasra')
    name_english_v2 = "v2"
    name_persian_v2 = "نسل دو";
    create_folder_with_meta_json(save_directory_v2,name_english_v2,name_persian_v2)

    # خواندن داده‌ها از شیت اول و سوم
    # first_sheet_data = data['v1']
    second_sheet_data = data['v2']
    third_sheet_data = data['extracted_links']

    english_root = ""
    # بررسی وجود ستون 'Reference'
    for index, row in second_sheet_data.iterrows():
        title = row['Title']
        
        if 'Reference' in row:
            reference = row['Reference']
        else:
            reference = None  # یا می‌توانید مقدار پیش‌فرض دیگری تعیین کنید

        is_page = True if row['Persian'] == "page" else False
        # type = row['Type']
        # hidden = row['Hidden']
        # toc = row['TOC']

        if not is_page:
            # تبدیل persian_name به رشته در صورت نیاز
            persian_name = str(row['Title'])
            persian_name = persian_name.replace('_', ' ')
            english_name = convert_persian_to_english(persian_name)
            english_root = english_name
            kasra_folder_path = os.path.join(save_directory, 'kasra', 'v2')
            # بررسی وجود پوشه kasra و ایجاد آن در صورت عدم وجود
            if not os.path.exists(kasra_folder_path):
                os.makedirs(kasra_folder_path)
            
            try: 
                # ایجاد پوشه با نام انگلیسی و فارسی در پوشه kasra
                create_folder_with_meta_json(kasra_folder_path, english_name, persian_name)
                # create_folder_with_meta_json(save_directory_v2 + name_english, english_name, persian_name)
            except Exception as e:
                print(f"خطا در ایجاد پوشه '{english_name}': {e}")

            # create_folder_with_meta_json(save_directory_v2,english_name,persian_name)
        else: # page
            # if(reference != None):
            
            reference = reference.replace('_', ' ')
            reference = reference.replace('.html', '')
            english_reference = convert_persian_to_english(reference)
            save_directory_ = os.path.join(kasra_folder_path,english_root)
            create_folder_with_meta_json(save_directory_, english_reference, reference)

        # جستجو در third_sheet_data با استفاده از index
        # if index < len(third_sheet_data):
        #     near_folder = third_sheet_data.iloc[index]['nearFolder']
        #     full_url = third_sheet_data.iloc[index]['full_url']
        #     filename1 = third_sheet_data.iloc[index]['filename1']
        #     filename2 = third_sheet_data.iloc[index]['filename2']
        #     htm_name = third_sheet_data.iloc[index]['htmName']

        #     # اینجا می‌توانید با داده‌ها کار کنید
        #     print(f"عنوان: {title}, مرجع: {reference}, صفحه یا بوک {is_page}, پوشه نزدیک: {near_folder}, URL کامل: {full_url}, نام فایل 1: {filename1}, نام فایل 2: {filename2}, نام HTML: {htm_name}")

    

    # # بررسی وجود nearFolder در ستون htmName شیت سوم
    # if any(third_sheet_data['htmName'] == near_folder):
    #     # دانلود فایل HTML
    #     html_url = second_sheet_data.iloc[0]['htmlUrl']  # فرض می‌کنیم که آدرس HTML در شیت اول موجود است
    #     html_file_path = os.path.join(base_folder, f"{near_folder}.html")
        
    #     response = requests.get(html_url)
    #     with open(html_file_path, 'wb') as html_file:
    #         html_file.write(response.content)
    #     print(f"📄 فایل HTML دانلود شد: {html_file_path}")

    #     # دانلود مدیاها
    #     media_urls = second_sheet_data.iloc[0]['mediaUrls'].split(',')  # فرض می‌کنیم که آدرس‌های مدیا در یک ستون به صورت کاما جدا شده‌اند
    #     media_folder = os.path.join(static_img_folder, 'media')
    #     os.makedirs(media_folder, exist_ok=True)

    #     for media_url in media_urls:
    #         media_response = requests.get(media_url.strip())
    #         media_file_name = os.path.basename(media_url.strip())
    #         media_file_path = os.path.join(media_folder, media_file_name)
    #         with open(media_file_path, 'wb') as media_file:
    #             media_file.write(media_response.content)
    #         print(f"📦 مدیا دانلود شد: {media_file_path}")
    # else:
    #     print("❌ هیچ موردی با nearFolder پیدا نشد.")












