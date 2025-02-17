import { useState } from "react";
import Fuse from "fuse.js";

const data = [
  { title: "نصب و راه‌اندازی", content: "راهنمای نصب نرم‌افزار" },
  { title: "ساختار پروژه", content: "بررسی فایل‌ها و پوشه‌ها" }
];

const fuse = new Fuse(data, {
  keys: ["title", "content"],
  threshold: 0.3,
});

export default function Search() {
  const [query, setQuery] = useState("");
  const results = fuse.search(query);
  
  return (
    <div>
      <input
        type="text"
        placeholder="جستجو..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-2 w-full rounded"
      />
      {query ? (
        results.length > 0 ? (
          <ul className="mt-4">
            {results.map(({ item }, index) => (
              <li key={index} className="p-3 hover:bg-gray-50 rounded-lg mb-2 border">
                <h3 className="font-bold text-lg mb-1">{item.title}</h3>
                <p className="text-gray-600">{item.content}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-center text-gray-500 mt-4">نتیجه‌ای یافت نشد</p>
        )
      ) : null}
    </div>
  );
}
