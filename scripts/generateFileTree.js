const fs = require('fs');
const path = require('path');

const docsPath = path.join(process.cwd(), 'pages'); 

function getDirectoryStructure(dirPath) {
    let result = [];
    const items = fs.readdirSync(dirPath, { withFileTypes: true });

    // بررسی اینکه آیا _meta.json در این پوشه وجود دارد
    const metaFilePath = path.join(dirPath, '_meta.json');
    let metaData = {};
    if (fs.existsSync(metaFilePath)) {
        try {
            metaData = JSON.parse(fs.readFileSync(metaFilePath, 'utf8'));
        } catch (error) {
            console.error(`❌ خطا در خواندن فایل _meta.json در ${dirPath}:`, error);
        }
    }

    items.forEach((item) => {
        const itemPath = path.join(dirPath, item.name);

        if (item.isDirectory()) {
            let displayName = metaData[item.name] || item.name; // اگر مقدار متا وجود داشت، جایگزین شود

            // دریافت فرزندان این پوشه
            const children = getDirectoryStructure(itemPath);

            // شمارش فقط فایل‌های واقعی و پوشه‌های داخلی، بدون در نظر گرفتن index.mdx و _meta.json
            const validChildren = fs.readdirSync(itemPath).filter(
                (file) => !["index.mdx", "_meta.json"].includes(file)
            ).length;

            result.push({
                name: displayName,
                realName: item.name, // نام واقعی پوشه (برای لینک‌دهی)
                type: 'folder',
                children: children.length > 0 ? children : undefined, // اگر children خالی بود، مقداردهی نشود
                count: validChildren, // تعداد فایل‌ها و پوشه‌های معتبر داخلی
            });
        } else if (!["index.mdx", "_meta.json", "404.mdx", "_app.js", "[slug].js"].includes(item.name)) { // حذف فایل‌های خاص
            result.push({
                name: item.name,
                type: 'file',
            });
        }
    });

    return result;
}

// تولید فایل JSON
const fileTree = getDirectoryStructure(docsPath);
fs.writeFileSync(path.join(process.cwd(), 'public', 'fileTree.json'), JSON.stringify(fileTree, null, 2));

console.log('✅ File tree has been generated!');
