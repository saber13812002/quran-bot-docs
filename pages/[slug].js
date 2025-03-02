import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const SlugPage = ({ title }) => {
  return (
    <div>
      <h1>{title}</h1>
    </div>
  );
};

export const getStaticProps = async (context) => {
  const { slug } = context.params;


  
  // Exclude 404 and about from being treated as dynamic pages
  if (slug === '404' || slug === 'about') {
    return { notFound: true };
  }

  const filePath = path.join(process.cwd(), 'pages', `${slug}.mdx`); // مسیر فایل MDX

  // بررسی اینکه آیا فایل وجود دارد یا خیر
  if (!fs.existsSync(filePath)) {
    return {
      notFound: true, // در صورتی که فایل وجود نداشت، صفحه 404 نمایش داده می‌شود.
    };
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const { data } = matter(content);
  const titleMatch = content.match(/^#\s+(.*)$/m);
  const title = titleMatch ? titleMatch[1] : data.title || 'Untitled';

  return {
    props: {
      title, // انتقال عنوان به کامپوننت
    },
  };
};

export const getStaticPaths = async () => {
  const files = fs.readdirSync(path.join(process.cwd(), 'pages'))
    .filter(file => file.endsWith('.mdx'))
    .filter(file => !['404.mdx', 'about.mdx'].includes(file)); // Exclude static pages

  const paths = files.map(file => ({
    params: { slug: file.replace('.mdx', '') }, // حذف .mdx از نام فایل برای استفاده به عنوان slug
  }));

  return {
    paths,
    fallback: false, // همه صفحات باید از قبل ساخته شوند
  };
};

export default SlugPage;
