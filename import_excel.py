import pandas as pd
import os
import requests
from urllib.parse import urljoin
import json

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

    print(english_name)
    if not os.path.exists(english_name):
        os.makedirs(english_name)
        print(f"📁 پوشه '{english_name}' ایجاد شد.")
    else:
        print(f"📁 پوشه '{english_name}' قبلاً وجود دارد.")

    meta_file_path = os.path.join(save_directory, english_name, '_meta.json')
    print(meta_file_path)
    if not os.path.exists(meta_file_path):
        meta_content = {
            english_name: persian_name
        }
        
        with open(meta_file_path, 'w', encoding='utf-8') as meta_file:
            json.dump(meta_content, meta_file, ensure_ascii=False, indent=4)
        print(f"📄 فایل '_meta.json' ایجاد شد: {meta_file_path}")
    else:
        print("📁 فایل '_meta.json' قبلاً وجود دارد.")
    # os.makedirs(base_folder, exist_ok=True)    

def throw(near_folder):
    raise near_folder
# main

if __name__ == "__main__":
    file_path = 'Table Of Contents.report.xlsx'
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

    save_directory_v1 = os.path.join(save_directory, 'kasra')
    name_english_v1 = "v1"
    name_persian_v1 = "نسل دوم";
    create_folder_with_meta_json(save_directory_v1,name_english_v1,name_persian_v1)


    # خواندن داده‌ها از شیت اول و سوم
    first_sheet_data = data['v1']
    third_sheet_data = data['extracted_links']

    for index, row in first_sheet_data.iterrows():
        title = row['Title']
        reference = row['Reference']
        perian_type = row['Perian Type']
        hidden = row['Hidden']

        # جستجو در third_sheet_data با استفاده از index
        if index < len(third_sheet_data):
            near_folder = third_sheet_data.iloc[index]['nearFolder']
            full_url = third_sheet_data.iloc[index]['full_url']
            filename1 = third_sheet_data.iloc[index]['filename1']
            filename2 = third_sheet_data.iloc[index]['filename2']
            htm_name = third_sheet_data.iloc[index]['htmName']

            # اینجا می‌توانید با داده‌ها کار کنید
            print(f"عنوان: {title}, مرجع: {reference}, نوع: {perian_type}, پنهان: {hidden}, پوشه نزدیک: {near_folder}, URL کامل: {full_url}, نام فایل 1: {filename1}, نام فایل 2: {filename2}, نام HTML: {htm_name}")

    

    # # بررسی وجود nearFolder در ستون htmName شیت سوم
    # if any(third_sheet_data['htmName'] == near_folder):
    #     # دانلود فایل HTML
    #     html_url = first_sheet_data.iloc[0]['htmlUrl']  # فرض می‌کنیم که آدرس HTML در شیت اول موجود است
    #     html_file_path = os.path.join(base_folder, f"{near_folder}.html")
        
    #     response = requests.get(html_url)
    #     with open(html_file_path, 'wb') as html_file:
    #         html_file.write(response.content)
    #     print(f"📄 فایل HTML دانلود شد: {html_file_path}")

    #     # دانلود مدیاها
    #     media_urls = first_sheet_data.iloc[0]['mediaUrls'].split(',')  # فرض می‌کنیم که آدرس‌های مدیا در یک ستون به صورت کاما جدا شده‌اند
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












