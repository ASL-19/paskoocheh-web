import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppGuideListItem from "src/components/App/AppTabContent/AppHowToUse/AppGuideListItem";
import { GqlGuide } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";

const container = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const AppGuideList: StylableFC<{
  guides: Array<GqlGuide>;
}> = memo(({ className, guides }) => {
  const { AppHowToUse: strings } = useAppStrings();

  return (
    <div className={className} css={container}>
      <h1 css={paragraphP2SemiBold}>{strings.guide}</h1>

      {guides.map((guide) => (
        <AppGuideListItem guide={guide} key={guide.id} />
      ))}
    </div>
  );
});

AppGuideList.displayName = "AppGuideList";

export default AppGuideList;
