import fs from 'fs';
import path from 'path';
import matter from 'gray-matter'; // برای خواندن front matter
import { useEffect, useState } from 'react';

const SlugPage = ({ title }) => {
  return (
    <div>
      <h1>{title}</h1> {/* نمایش عنوان */}
      {/* محتوای دیگر صفحه */}
    </div>
  );
};

export const getStaticProps = async (context) => {
  const { slug } = context.params; // دریافت slug از URL

  const filePath = path.join(process.cwd(), 'pages', `${slug}.mdx`); // مسیر فایل MDX

  // بررسی اینکه آیا فایل وجود دارد یا خیر
  if (!fs.existsSync(filePath)) {
    return {
      notFound: true, // در صورتی که فایل وجود نداشت، صفحه 404 نمایش داده می‌شود.
    };
  }

  const content = fs.readFileSync(filePath, 'utf8'); // خواندن محتوای فایل

  // استخراج front matter با استفاده از gray-matter
  const { data } = matter(content); // استخراج front matter

  // استخراج عنوان از اولین تگ h1 (یعنی اولین #)
  const titleMatch = content.match(/^#\s+(.*)$/m); // پیدا کردن اولین تگ #
  const title = titleMatch ? titleMatch[1] : data.title || 'بدون عنوان'; // اگر # یافت شد، عنوانش را می‌گیریم

  return {
    props: {
      title, // انتقال عنوان به کامپوننت
    },
  };
};

export const getStaticPaths = async () => {
  // فرض کنید همه فایل‌های MDX در پوشه "pages" قرار دارند.
  const files = fs.readdirSync(path.join(process.cwd(), 'pages')).filter(file => file.endsWith('.mdx'));
  
  const paths = files.map(file => ({
    params: { slug: file.replace('.mdx', '') }, // حذف .mdx از نام فایل برای استفاده به عنوان slug
  }));

  return {
    paths,
    fallback: false, // همه صفحات باید از قبل ساخته شوند
  };
};

export default SlugPage;
