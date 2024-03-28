import { asType } from "@asl-19/js-utils";

import { GqlVersion } from "src/generated/graphQl";
import toolTestDataBySlug from "src/test/data/toolTestDataBySlug";
import versionPreviewTestDataBySlug from "src/test/data/versionPreviewTestDataBySlug";
import versionReviewsById from "src/test/data/versionReviewsById";

const versionTestDataBySlug = {
  // cSpell:disable
  "beepass-vpn": asType<GqlVersion>({
    ...versionPreviewTestDataBySlug["beepass-vpn"],
    averageRating: {
      id: "VmVyc2lvblJhdGluZ05vZGU6MzM1",
      lastModified: "2021-05-31T16:30:10.823823+00:00",
      platformName: "android",
      ratingCount: 81,
      starRating: 3.7,
      toolName: "BeePass VPN",
    },
    canGenerateTempS3Url: true,
    created: "2021-01-07T09:32:13.062400+00:00",
    deliveryEmail: "beepassvpn-android@paskoocheh.com",
    downloadCount: 3998,
    downloadUrl:
      "https://play.google.com/store/apps/details?id=com.beepassvpn.free.vpn.secure",
    faqUrl: "",
    guides: {
      edges: [
        {
          node: {
            body: "<p>This is a test for BeePass Vpn</p>",
            headline: "BeePass VPN Guide",
            id: "R3VpZGVOb2RlOjIz",
            language: "en",
            lastModified: "2023-09-28T20:02:26.940750+00:00",
            order: 1,
            pk: 23,
            slug: null,
            video:
              "video/X2Convert.com_shortest_video_on_youtube_part_2_3788880989907131245.26a87c83fd45.mp4",
          },
        },
      ],
    },
    guideUrl: "",
    id: "VmVyc2lvbk5vZGU6Mzgz",
    lastModified: "2022-08-11T18:44:05.949302+00:00",
    packageName: "com.beepassvpn.free.vpn.secure",
    pk: 383,
    // platform: platformTestDataBySlug["android"],
    releaseDate: "2022-06-16T19:30:00+00:00",
    releaseUrl: null,
    reviews: {
      edges: [
        {
          node: versionReviewsById.review1,
        },
      ],
      pageInfo: {
        hasNextPage: false,
      },
      totalCount: 1,
    },
    tool: toolTestDataBySlug["beepass-vpn"],
    tutorials: {
      edges: [
        {
          node: {
            id: "VHV0b3JpYWxOb2RlOjk=",
            language: "fa",
            lastModified: "2021-01-22T14:53:41.309045+00:00",
            order: 1,
            pk: 9,
            title: "نحوه درخواست سرور از طریق ایمیل",
            video: "video/BeePassVPN-EmailBot-Instruction.c5d626afb03d.mp4",
            videoLink: null,
          },
        },
      ],
    },
    versionNumber: "1.2.3",
    video: "",
    videoLink: null,
  }),
  // cSpell:enable
};

export default versionTestDataBySlug;
