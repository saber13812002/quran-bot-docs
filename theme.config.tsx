import React from "react";
import { DocsThemeConfig } from "nextra-theme-docs";
import { useConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  direction: "rtl",
  navbar: {
  },
  logo: (
    <>
      <img
        style={{ fontFamily: 'Anjoman', fontSize: '1.5rem', color: 'blue' , width: "30px" }}
        src="assets/img/depna.png"
        alt="depna"
      />
      کسرا نسل دوم
    </>
  ),
  // project: {
  //   link: "https://gitlab.depna.com/s.tabatabaei/kasra-nextra-doc",
  // },
  // chat: {
  //   link: "https://www.youtube.com/@JBWEBDEVELOPER",
  //   icon: (
  //     <>
  //       <img
  //         style={{ width: "35px" }}
  //         src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png"
  //         alt=""
  //       />
  //     </>
  //   ),
  // },
  docsRepositoryBase: "https://gitlab.depna.com/s.tabatabaei/kasra-nextra-doc",
  footer: {
    text: "هولدینگ مهیمن - محصول کسرا نسل دوم",
  },
  useNextSeoProps() {
    return {
      titleTemplate: '%s – عنوان سایت شما'
    }
  },
  search: {
    placeholder: 'جستجو...',
    loading: 'در حال جستجو...',
    error: 'خطا در جستجو',
    emptyResult: 'نتیجه‌ای یافت نشد'
  }
};

export default config;
