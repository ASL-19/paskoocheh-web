import { asType } from "@asl-19/js-utils";

import { GqlTool } from "src/generated/graphQl";
import toolPreviewTestDataBySlug from "src/test/data/toolPreviewTestDataBySlug";
import versionPreviewTestDataBySlug from "src/test/data/versionPreviewTestDataBySlug";

const toolTestDataBySlug = {
  // cSpell:disable
  "beepass-vpn": asType<GqlTool>({
    ...toolPreviewTestDataBySlug["beepass-vpn"],
    blog: null,
    contactEmail: null,
    contactUrl: null,
    created: "2021-01-07T09:30:19.751978+00:00",
    facebook: null,
    faqs: { edges: [] },
    info: {
      edges: [
        {
          node: {
            company: "BeePassVPN",
            description: `<p>فیلترشکن BeePass، یک فیلترشکن رایگان، ساده و امن است که با تمرکز بر حفظ حریم خصوصی شما طراحی شده است. BeePass برای دور زدن سانسور و فیلترینگ در اینترنت به شما کمک می‌کند و حریم خصوصی آنلاین شما را بهبود می‌بخشد. </p>
            <p>🐝 ویز ویز 😁</p>
            <p>😎 BeePass یک فیلترشکن متفاوت است. </p>
            <p>💛 فیلترشکن BeePass رایگان است. تبلیغات آزاردهنده و دوره‌ی آزمایشی رایگان ندارد. </p>
            <p>♾ فیلترشکن BeePass نامحدود است. این فیلترشکن محدودیت حجمی ندارد و شما می‌توانید برای تمام فعالیت‌های اینترنتی خود از آن استفاده کنید. </p>
            <p>🔐 فیلترشکن BeePass امن است. سیستم رمزگذاری قوی آن از ارتباطات و وب‌گردی شما در برابر چشمان کنجکاو دیگر افراد یا سازمان‌ها محافظت می‌کند. ما نسبت به حفظ حریم خصوصی شما حساس هستیم و شما هم باید برای این موضوع ارزش قائل شوید. </p>
            <p>📖 BeePass یک فیلترشکن متن‌باز است. و توسط شرکت‌های امنیتی بررسی ممیزی شده است.</p>
            <p>🛡️ فیلترشکن BeePass در برابر سانسور مقاوم است. ما برای این کار وقت می‌گذاریم تا شما مجبور به انجام آن نباشید. </p>
            <p>🔑 با فیلترشکن BeePass سانسور را دور بزنید.</p>`,
            id: "SW5mb05vZGU6MjIx",
            language: "fa",
            lastModified: "2021-01-07T09:34:25.886716+00:00",
            name: "BeePass VPN",
            pk: 221,
            promoText: "BeePassVpn",
            seoDescription: "beepass vpn",
            tool: {
              website: "paskoocheh.com",
            },
          },
        },
      ],
    },
    lastModified: "2024-01-08T21:36:08.370576+00:00",
    lastUpdate: "2024-01-08T21:36:08.370595+00:00",
    source: null,
    teamAnalysis: {
      categoryAnalysis: [
        {
          id: "Q2F0ZWdvcnlBbmFseXNpc05vZGU6MQ==",
          pk: 1,
          rating: 9.9,
          ratingCategory: {
            id: "UmF0aW5nQ2F0ZWdvcnlOb2RlOjE=",
            name: "Speed",
            nameAr: "Speed",
            nameFa: "Speed",
            slug: "Speed",
          },
        },
        {
          id: "Q2F0ZWdvcnlBbmFseXNpc05vZGU6Mg==",
          pk: 2,
          rating: 5.0,
          ratingCategory: {
            id: "UmF0aW5nQ2F0ZWdvcnlOb2RlOjI=",
            name: "Stability",
            nameAr: "Stability",
            nameFa: "Stability",
            slug: "stability",
          },
        },
      ],
      cons: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      id: "VGVhbUFuYWx5c2lzTm9kZTox",
      pk: 1,
      pros: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
      review: "This a really good app",
    },
    trusted: true,
    twitter: "",
    versions: {
      edges: [
        {
          node: versionPreviewTestDataBySlug["beepass-vpn"],
        },
      ],
    },
    website: "https://beepassvpn.com/fa/",
  }),
  // cSpell:enable
};

export default toolTestDataBySlug;
