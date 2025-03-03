const withNextra = require("nextra")({
  theme: "nextra-theme-docs",
  themeConfig: "./theme.config.tsx",
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export", // Enables full static export
  trailingSlash: false, // Ensures correct index.html placement
  images: {
    unoptimized: true, // Required for static exports
  },
  reactStrictMode: true,
};

module.exports = withNextra(nextConfig);
