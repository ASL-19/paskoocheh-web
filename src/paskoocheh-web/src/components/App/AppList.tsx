import { StylableFC } from "@asl-19/react-dom-utils";
import { css, SerializedStyles } from "@emotion/react";
import { memo } from "react";

import AppListItem from "src/components/App/AppListItem";
import { GqlVersionPreview } from "src/generated/graphQl";
import { threeColumnGridContainer } from "src/styles/generalStyles";
import versionPreviewTestDataBySlug from "src/test/data/versionPreviewTestDataBySlug";
import { ValidVersionPreview } from "src/types/appTypes";
import { HeadingLevel } from "src/types/miscTypes";
import { breakpointStyles } from "src/utils/media/media";

const container = ({ hasItemLogos }: { hasItemLogos?: boolean }) =>
  css(
    threeColumnGridContainer,
    breakpointStyles({
      singleColumn: {
        lt: {
          gap: "1rem",
          gridTemplateColumns: `repeat(auto-fill, minmax(${
            hasItemLogos ? "13rem" : "9rem"
          }, 1fr))`,
        },
      },
    }),
  );

export const dummyVersionPreviews: Array<GqlVersionPreview> = Array.from({
  length: 6,
}).map((item, index) => ({
  ...versionPreviewTestDataBySlug["beepass-vpn"],
  id: `${index}`,
}));

const AppList: StylableFC<{
  hasItemLogos?: boolean;
  hasItemPromoImages?: boolean;
  itemHeadingLevel: HeadingLevel;
  itemLogoCss?: SerializedStyles;
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(
  ({
    hasItemLogos = true,
    hasItemPromoImages = false,
    itemHeadingLevel,
    itemLogoCss,
    versionPreviews,
    ...remainingProps
  }) => (
    <ul css={container({ hasItemLogos })} {...remainingProps}>
      {versionPreviews.map((app) => (
        <AppListItem
          versionPreview={app}
          headingLevel={itemHeadingLevel}
          hasLogo={hasItemLogos}
          hasPromoImage={hasItemPromoImages}
          logoCss={itemLogoCss}
          key={app.id}
        />
      ))}
    </ul>
  ),
);

AppList.displayName = "AppList";

export default AppList;
