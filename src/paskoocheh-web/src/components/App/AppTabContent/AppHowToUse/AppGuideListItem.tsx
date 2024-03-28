import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import HtmlContent from "src/components/HtmlContent";
import MediaVideo from "src/components/MediaVideo";
import { GqlGuide } from "src/generated/graphQl";
import { paragraphP2SemiBold } from "src/styles/typeStyles";

const container = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const AppGuideListItem: StylableFC<{
  guide: GqlGuide;
}> = memo(({ className, guide }) => {
  return (
    <div className={className} css={container}>
      <h2 css={paragraphP2SemiBold}>{guide.headline}</h2>

      <HtmlContent dangerousHtml={guide.body ?? ""} />

      {guide.video && <MediaVideo video={guide.video ?? ""} />}
    </div>
  );
});

AppGuideListItem.displayName = "AppGuideListItem";

export default AppGuideListItem;
