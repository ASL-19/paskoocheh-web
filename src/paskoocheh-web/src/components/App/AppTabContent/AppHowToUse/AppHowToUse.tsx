import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppGuideList from "src/components/App/AppTabContent/AppHowToUse/AppGuideList";
import AppTutorialList from "src/components/App/AppTabContent/AppHowToUse/AppTutorialList";
import { GqlGuide, GqlTutorial } from "src/generated/graphQl";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type AppHowToUseStrings = {
  guide: string;
  howToUse: string;
  introduction: string;
  noGuideOrTutorials: string;
  tutorials: string;
};

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  display: "flex",
  flexDirection: "column",
  padding: "1.25rem",
  rowGap: "1.25rem",
});

const AppHowToUse: StylableFC<{
  guides: Array<GqlGuide>;
  tutorials: Array<GqlTutorial>;
}> = memo(({ guides, tutorials, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();

  const { AppHowToUse: strings } = useAppStrings();

  const sortedGuides = guides
    .filter((guide) => guide.language === localeCode)
    .sort((a, b) => a.order ?? 0 - (b.order ?? 0));

  const sortedTutorials = tutorials
    .filter((guide) => guide.language === localeCode)
    .sort((a, b) => a.order ?? 0 - (b.order ?? 0));

  if (sortedGuides.length === 0 && sortedTutorials.length === 0)
    return <div>{strings.noGuideOrTutorials}</div>;
  return (
    <div css={container} {...remainingProps}>
      {sortedGuides.length > 0 && <AppGuideList guides={sortedGuides} />}

      {sortedTutorials.length > 0 && (
        <AppTutorialList tutorials={sortedTutorials} />
      )}
    </div>
  );
});

AppHowToUse.displayName = "AppHowToUse";

export default AppHowToUse;
