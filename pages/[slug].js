import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { useRouter } from 'next/router';

export default function DocPage({ content }) {
  const router = useRouter();
  
  if (router.isFallback) {
    return <div>در حال بارگذاری...</div>;
  }

  return (
    <div className="prose prose-lg">
      <div dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
}

export async function getStaticPaths() {
  const files = fs.readdirSync(path.join("pages"));
  const paths = files
    .filter(file => file.endsWith(".mdx"))
    .map(file => ({ params: { slug: file.replace(".mdx", "") } }));

  return { paths, fallback: false };
}

export async function getStaticProps({ params }) {
  const filePath = path.join("pages", `${params.slug}.mdx`);
  const fileContent = fs.readFileSync(filePath, "utf-8");
  const { content } = matter(fileContent);

  return { props: { content } };
}
