import React from "react";
import { DocsThemeConfig } from "nextra-theme-docs";
import Search from "./components/Search";

const config: DocsThemeConfig = {
  direction: "rtl",
  navbar: {
    extraContent: <Search />
  },
  logo: (
    <>
      <img
        style={{ fontFamily: 'Anjoman', fontSize: '1.5rem', color: 'blue' , width: "80px" }}
        src="https://logowik.com/content/uploads/images/nextjs2106.logowik.com.webp"
        alt=""
      />
    </>
  ),
  project: {
    link: "https://gitlab.depna.com/s.tabatabaei/kasra-nextra-doc",
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
  docsRepositoryBase: "https://gitlab.depna.com/s.tabatabaei/kasra-nextra-doc",
  footer: {
    text: "کسرا نسل دو",
  },
};

export default config;
