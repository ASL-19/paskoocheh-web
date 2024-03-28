import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppAdditionalInfoListItem from "src/components/App/AppTabContent/AppAdditionalInfo/AppAdditionalInfoListItem";
import AppAdditionalInfoProductDetails from "src/components/App/AppTabContent/AppAdditionalInfo/AppAdditionalInfoProductDetails";
import { GqlInfo } from "src/generated/graphQl";
import { ValidVersion } from "src/types/appTypes";
import colors from "src/values/colors";

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  padding: "1.25rem",
});

const listContainer = css({
  "& > li:not(:last-of-type)": {
    borderBottom: `solid 1px ${colors.secondary50}`,
  },
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const listItem = css({
  display: "flex",
  flexDirection: "column",
  paddingBottom: "1.25rem",
  rowGap: "1.25rem",
});

const AppAdditionalInfo: StylableFC<{
  infos: Array<GqlInfo>;
  version: ValidVersion;
}> = memo(({ infos, version, ...remainingProps }) => (
  <div css={container} {...remainingProps}>
    <ul css={listContainer}>
      {infos.map((info) => (
        <AppAdditionalInfoListItem
          info={info}
          key={info.id}
          tool={version.tool}
          css={listItem}
        />
      ))}

      {version && (
        <AppAdditionalInfoProductDetails version={version} css={listItem} />
      )}
    </ul>
  </div>
));

AppAdditionalInfo.displayName = "AppAdditionalInfo";

export default AppAdditionalInfo;
