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
  
  // return (
  //   <div>
  //     <input
  //       type="text"
  //       placeholder="جستجو..."
  //       value={query}
  //       onChange={(e) => setQuery(e.target.value)}
  //       className="border p-2 w-full rounded"
  //     />
  //     <ul>
  //       {results.map(({ item }, index) => (
  //         <li key={index} className="mt-2">
  //           <strong>{item.title}</strong>: {item.content}
  //         </li>
  //       ))}
  //     </ul>
  //   </div>
  // );
  return (
    <div className="w-full max-w-xl mx-auto p-4">
      <input
        type="text" 
        placeholder="جستجو..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="border p-3 w-full rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
      <ul className="mt-4 space-y-3">
        {results.map(({ item }, index) => (
          <li key={index} className="p-3 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-lg font-bold text-gray-900 mb-1">{item.title}</h3>
            <p className="text-gray-600">{item.content}</p>
          </li>
        ))}
        {query && !results.length && (
          <li className="text-center text-gray-500 p-4">
            نتیجه‌ای یافت نشد
          </li>
        )}
      </ul>
    </div>
  );
}
