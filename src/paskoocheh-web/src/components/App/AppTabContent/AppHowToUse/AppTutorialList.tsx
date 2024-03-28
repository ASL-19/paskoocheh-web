import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppTutorialListItem from "src/components/App/AppTabContent/AppHowToUse/AppTutorialListItem";
import { GqlTutorial } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";

const container = css(paragraphP2SemiBold, {
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const AppTutorialList: StylableFC<{
  tutorials: Array<GqlTutorial>;
}> = memo(({ className, tutorials }) => {
  const { AppHowToUse: strings } = useAppStrings();

  return (
    <div className={className} css={container}>
      <h2>{strings.tutorials}</h2>

      {tutorials.map((tutorial) => (
        <AppTutorialListItem tutorial={tutorial} key={tutorial.id} />
      ))}
    </div>
  );
});

AppTutorialList.displayName = "AppTutorialList";

export default AppTutorialList;
