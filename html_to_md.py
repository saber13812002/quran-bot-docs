import os
import requests
import html2text
from urllib.parse import urlparse

# List of URLs to download
urls = [
    "https://nextra.site/docs",
    "https://nextra.site/docs#nextra-skip-nav",
    "https://nextra.site/docs/file-conventions",
    "https://nextra.site/docs/file-conventions#nextra-skip-nav",
    "https://nextra.site/docs/file-conventions/page-file",
    "https://nextra.site/docs/file-conventions/meta-file",
    "https://nextra.site/docs/file-conventions/mdx-components-file",
    "https://nextra.site/docs/file-conventions/content-directory",
    "https://nextra.site/docs/file-conventions/src-directory",
    "https://nextra.site/docs/guide",
    "https://nextra.site/docs/guide/markdown",
    "https://nextra.site/docs/guide/syntax-highlighting",
    "https://nextra.site/docs/guide/link",
    "https://nextra.site/docs/guide/image",
    "https://nextra.site/docs/guide/ssg",
    "https://nextra.site/docs/guide/i18n",
    "https://nextra.site/docs/guide/custom-css",
    "https://nextra.site/docs/guide/static-exports",
    "https://nextra.site/docs/guide/search",
    "https://nextra.site/docs/guide/github-alert-syntax",
    "https://nextra.site/docs/guide/turbopack",
    "https://nextra.site/docs/advanced",
    "https://nextra.site/docs/advanced/npm2yarn",
    "https://nextra.site/docs/advanced/mermaid",
    "https://nextra.site/docs/advanced/tailwind-css",
    "https://nextra.site/docs/advanced/latex",
    "https://nextra.site/docs/advanced/table",
    "https://nextra.site/docs/advanced/typescript",
    "https://nextra.site/docs/advanced/remote",
    "https://nextra.site/docs/advanced/playground",
    "https://nextra.site/docs/advanced/customize-the-cascade-layers",
    "https://nextra.site/docs/advanced/twoslash",
    "https://nextra.site/docs/built-ins",
    "https://nextra.site/docs/built-ins/banner",
    "https://nextra.site/docs/built-ins/head",
    "https://nextra.site/docs/built-ins/search",
    "https://nextra.site/docs/built-ins/bleed",
    "https://nextra.site/docs/built-ins/callout",
    "https://nextra.site/docs/built-ins/cards",
    "https://nextra.site/docs/built-ins/filetree",
    "https://nextra.site/docs/built-ins/steps",
    "https://nextra.site/docs/built-ins/table",
    "https://nextra.site/docs/built-ins/tabs",
    "https://nextra.site/docs/docs-theme",
    "https://nextra.site/docs/docs-theme/start",
    "https://nextra.site/docs/docs-theme/built-ins",
    "https://nextra.site/docs/docs-theme/built-ins/layout",
    "https://nextra.site/docs/docs-theme/built-ins/footer",
    "https://nextra.site/docs/docs-theme/built-ins/navbar",
    "https://nextra.site/docs/docs-theme/built-ins/not-found",
    "https://nextra.site/docs/docs-theme/api",
    "https://nextra.site/docs/blog-theme",
    "https://nextra.site/docs/blog-theme/start",
    "https://nextra.site/docs/blog-theme/get-posts-and-tags",
    "https://nextra.site/docs/blog-theme/posts",
    "https://nextra.site/docs/blog-theme/tags",
    "https://nextra.site/docs/blog-theme/rss",
    "https://nextra.site/docs/custom-theme",
    "https://nextra.site/docs#quick-start",
    "https://nextra.site/docs#faq",
    "https://nextra.site/docs#can-i-use-nextra-with-nextjs-pages-router",
    "https://nextra.site/docs#can-i-use-x-with-nextra",
    "https://nextra.site/docs/guide/tailwind-css",
    "https://nextra.site/docs#how-can-i-add-a-live-coding-component-in-nextra"
]

def get_filename(url):
    # Remove the fragment part if present
    base = url.split('#')[0]
    parsed = urlparse(base)
    path = parsed.path
    # If the path is empty or just '/', name the file "index.md"
    if not path or path == "/":
        filename = "index.md"
    else:
        # Use the last part of the path and ensure a .md extension
        filename = os.path.basename(path)
        if not filename.endswith(".md"):
            filename += ".md"
    return filename

# Directory to save downloaded files
output_dir = "downloaded_md_files"
os.makedirs(output_dir, exist_ok=True)

# Initialize the HTML to Markdown converter
converter = html2text.HTML2Text()
converter.ignore_links = False  # Change to True to ignore links if desired

for url in urls:
    try:
        print("Downloading:", url)
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        md_content = converter.handle(html)
        filename = get_filename(url)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        print("Saved:", filepath)
    except Exception as e:
        print("Error downloading", url, ":", e)
