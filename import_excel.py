import pandas as pd

def read_excel_data(file_path):
    # خواندن داده‌ها از فایل اکسل
    xls = pd.ExcelFile(file_path)
    
    # خواندن هر شیت به صورت دیکشنری
    sheets_data = {}
    for sheet_name in xls.sheet_names:
        sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
    
    return sheets_data

# استفاده از تابع برای خواندن داده‌ها
file_path = 'Table Of Contents.report.xlsx'
data = read_excel_data(file_path)

# نمایش داده‌های خوانده شده
for sheet, df in data.items():
    print(f"داده‌های شیت {sheet}:")
    print(df.head(300))  # نمایش 5 ردیف اول هر شیت
