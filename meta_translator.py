import os
import json

def extract_id_from_file(file_path):
    """این تابع برای استخراج _id از محتویات فایل استفاده می‌شود."""
    if not os.path.isfile(file_path):  # بررسی اینکه آیا file_path یک فایل است
        return None
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith('_id'):
                return line.strip()
    return None

def translate_meta(folder_path):
    # بررسی وجود پوشه
    if not os.path.exists(folder_path):
        print(f"پوشه {folder_path} وجود ندارد.")
        return

    # بررسی وجود فایل _meta.json
    meta_file_path = os.path.join(folder_path, '_meta.json')
    if not os.path.isfile(meta_file_path):
        # ایجاد فایل جدید به نام _meta.json
        meta_data = {}
        
        # لیست کردن فایل‌ها و پوشه‌ها
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # اگر پوشه باشد
            if os.path.isdir(item_path):
                # استخراج _id از فایل‌های داخل پوشه
                id_value = extract_id_from_file(item_path)
                if id_value:
                    meta_data[item] = id_value
                else:
                    meta_data[item] = "مقدار پیش‌فرض"  # مقدار پیش‌فرض در صورت عدم وجود _id

            # اگر فایل باشد و با .json تمام شود
            elif item.endswith('.json'):
                id_value = extract_id_from_file(item_path)
                if id_value:
                    meta_data[item] = id_value
                else:
                    meta_data[item] = "مقدار پیش‌فرض"  # مقدار پیش‌فرض در صورت عدم وجود _id

        # نوشتن داده‌ها در فایل _meta.json
        with open(meta_file_path, 'w', encoding='utf-8') as new_file:
            json.dump(meta_data, new_file, ensure_ascii=False, indent=4)
        print(f"فایل _meta.json در {folder_path} ایجاد شد.")

    # بررسی پوشه‌های داخلی
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            translate_meta(item_path)  # فراخوانی بازگشتی برای پوشه‌های داخلی

# مثال استفاده
if __name__ == "__main__":
    translate_meta("pages")  # مسیر پوشه مورد نظر را اینجا وارد کنید
