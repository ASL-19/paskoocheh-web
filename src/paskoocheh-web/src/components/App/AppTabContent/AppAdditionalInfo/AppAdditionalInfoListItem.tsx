import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import HtmlContent from "src/components/HtmlContent";
import { GqlInfo, GqlTool } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP1Regular, paragraphP2SemiBold } from "src/styles/typeStyles";

export type AppAdditionalInfoListItemStrings = {
  /**
   * Text for developer info
   */
  developerInformation: string;
  /**
   * Text for product description
   */
  productDescription: string;
};

const itemContainer = css(paragraphP1Regular, {
  display: "flex",
  gap: "0.25rem",
});

const AppAdditionalInfoListItem: StylableFC<{
  info: GqlInfo;
  tool: GqlTool;
}> = memo(({ info, tool, ...remainingProps }) => {
  const { AppAdditionalInfoListItem: strings, shared: sharedStrings } =
    useAppStrings();

  return (
    <li {...remainingProps}>
      <h2 css={paragraphP2SemiBold}>{strings.developerInformation}</h2>
      <p css={paragraphP1Regular}>{info.company}</p>

      {tool.contactEmail && (
        <p css={itemContainer}>
          <span>{sharedStrings.socialMediaPlatformNames.email}:</span>
          <a href={`mailto:${tool.contactEmail}`}>{tool.contactEmail}</a>
        </p>
      )}

      <h2 css={paragraphP2SemiBold}>{strings.productDescription}</h2>
      <HtmlContent dangerousHtml={info.description ?? ""} />
    </li>
  );
});

AppAdditionalInfoListItem.displayName = "AppAdditionalInfoListItem";

export default AppAdditionalInfoListItem;
