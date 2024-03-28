import { asType } from "@asl-19/js-utils";

import { GqlToolPreview } from "src/generated/graphQl";
import toolTypeTestDataBySlug from "src/test/data/toolTypeTestDataBySlug";
import versionTypeTestDataBySlug from "src/test/data/toolTypeTestDataBySlug";

const toolPreviewTestDataBySlug = {
  // cSpell:disable
  "beepass-vpn": asType<GqlToolPreview>({
    availablePlatforms: ["android"],
    featured: true,
    id: "VG9vbE5vZGU6MTQ2",
    images: [
      {
        height: 180,
        id: "VG9vbEltYWdlTm9kZTo5",
        image: "/media/img/logo.0b2c0e67da33.png",
        imageType: "logo",
        pk: 9,
        width: 180,
      },
    ],
    info: {
      edges: [
        {
          node: {
            promoText: "BeePassVpn",
          },
        },
      ],
    },
    name: "BeePass VPN",
    pk: 146,
    primaryTooltype: toolTypeTestDataBySlug.circumvention,
    slug: "beepass-vpn",
    toolTypes: [versionTypeTestDataBySlug.circumvention],
  }),
  // cSpell:enable
};

export default toolPreviewTestDataBySlug;
