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
      <ul>
        {results.map(({ item }, index) => (
          <li key={index} className="mt-2">
            <strong>{item.title}</strong>: {item.content}
          </li>
        ))}
      </ul>
    </div>
  );
}
