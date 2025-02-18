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
  docsRepositoryBase: "https://gitlab.depna.com/s.tabatabaei/kasra-nextra-doc/-/blob/main",
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
  },
  feedback: {
    content: 'ارسال بازخورد ←',
  },
  editLink: {
    text: 'ویرایش این صفحه'
  },
  toc: {
    title: 'در این صفحه'
  },
  gitTimestamp: ({ timestamp }) => {
    return <span>آخرین بروزرسانی در تاریخ {new Intl.DateTimeFormat('fa-IR').format(timestamp)}</span>
  },
  themeSwitch: {
    useOptions() {
      return {
        light: 'روشن',
        dark: 'تیره',
        system: 'سیستم'
      }
    }
  }
};

export default config;
