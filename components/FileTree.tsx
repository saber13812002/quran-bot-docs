import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Card } from "nextra/components"; // استفاده از Card از Nextra

interface FileNode {
  name: string; // نام نمایشی (فارسی از _meta.json یا نام پوشه)
  realName?: string; // نام واقعی پوشه برای لینک‌دهی
  type: "file" | "folder";
  children?: FileNode[];
  count?: number;
}

const FileTree: React.FC = () => {
  const [fileTree, setFileTree] = useState<FileNode[]>([]);
  const router = useRouter();

  // مسیر فعلی از `router.pathname`
  const currentPath = router.pathname.replace(/^\//, "").split("/").filter(Boolean);

  useEffect(() => {
    fetch("/fileTree.json")
      .then((res) => res.json())
      .then((data) => setFileTree(data));
  }, []);

  // تابع برای پیدا کردن سطح جاری در JSON
  const findCurrentLevel = (nodes: FileNode[], pathSegments: string[]): FileNode[] => {
    if (pathSegments.length === 0) return nodes;
    const nextSegment = pathSegments.shift();
    const nextNode = nodes.find((node) => node.type === "folder" && node.realName === nextSegment);
    return nextNode && nextNode.children ? findCurrentLevel(nextNode.children, pathSegments) : [];
  };

  const currentLevelNodes = findCurrentLevel(fileTree, [...currentPath]);

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">
        📂 {currentPath.length ? currentPath[currentPath.length - 1] : "صفحه اصلی"}
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {currentLevelNodes.length > 0 ? (
          currentLevelNodes
            .filter((node) => node.realName || node.name) // فیلتر گره‌های بدون مسیر
            .map((node, index) => {
              const realPath = node.realName || node.name;
              if (!realPath) return null; // جلوگیری از مقدار `undefined`

              // مسیر جدید برای لینک‌دهی
              const newPath = `/${[...currentPath, realPath].join("/")}`;

              return (
                <Card
                  key={index}
                  href={newPath} // لینک به جای Link اینجا میره
                  title={node.name} // نمایش نام فارسی
                  icon={node.type === "folder" ? "📁" : "📄"} // آیکون
                  arrow={false} // حذف فلش اضافه در لینک
                >
                  {node.type === "folder" ? (
                    <span className="text-gray-500">{node.count} آیتم</span>
                  ) : (
                    <span className="text-gray-700">{node.name.replace(".mdx", "")}</span>
                  )}
                </Card>
              );
            })
        ) : (
          <p className="text-gray-500">📂 هیچ فایل یا پوشه‌ای در این سطح وجود ندارد.</p>
        )}
      </div>
    </div>
  );
};

export default FileTree;
