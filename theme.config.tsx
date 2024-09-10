import React from "react";
import { DocsThemeConfig } from "nextra-theme-docs";

const config: DocsThemeConfig = {
  logo: (
    <>
      <img
        style={{ width: "80px" }}
        src="https://logowik.com/content/uploads/images/nextjs2106.logowik.com.webp"
        alt=""
      />
    </>
  ),
  project: {
    link: "https://github.com/shuding/nextra-docs-template",
  },
  chat: {
    link: "https://www.youtube.com/@JBWEBDEVELOPER",
    icon: (
      <>
        <img
          style={{ width: "35px" }}
          src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png"
          alt=""
        />
      </>
    ),
  },
  docsRepositoryBase: "https://github.com/shuding/nextra-docs-template",
  footer: {
    text: "Nextra Docs Template",
  },
};

export default config;
