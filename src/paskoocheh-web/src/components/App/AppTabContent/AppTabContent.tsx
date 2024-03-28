import { invisible } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, useId } from "react";
import { match } from "ts-pattern";

import AppAdditionalInfo from "src/components/App/AppTabContent/AppAdditionalInfo/AppAdditionalInfo";
import AppFaqs from "src/components/App/AppTabContent/AppFaqs/AppFaqs";
import AppHowToUse from "src/components/App/AppTabContent/AppHowToUse/AppHowToUse";
import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import AppRatingAndReviews from "src/components/App/AppTabContent/AppRatingsAndReviews/AppRatingAndReviews";
import AppTeamAnalysis from "src/components/App/AppTabContent/AppTeamAnalysis/AppTeamAnalysis";
import { AppDetailsSectionId } from "src/components/App/appValues";
import { GqlInfo } from "src/generated/graphQl";
import {
  tabContainerActive,
  tabContainerInactive,
  tabsContainer,
} from "src/styles/tabStyles";
import { ValidVersion } from "src/types/appTypes";

const AppTabContent: StylableFC<{
  activeSectionId: AppDetailsSectionId;
  currentPlatformVersion: ValidVersion;
  infos: Array<GqlInfo>;
  navLinkInfos: Array<AppNavLinkInfo<AppDetailsSectionId>>;
}> = memo(
  ({
    activeSectionId,
    className,
    currentPlatformVersion,
    infos,
    navLinkInfos,
  }) => {
    const id = useId();

    const teamAnalysis = currentPlatformVersion.tool.teamAnalysis;

    const faqs = (currentPlatformVersion.tool.faqs?.edges || []).map(
      (edge) => edge.node,
    );

    const guides = (currentPlatformVersion.guides?.edges || []).map(
      (edge) => edge.node,
    );

    const tutorials = (currentPlatformVersion.tutorials?.edges || []).reduce(
      (acc, edge) => (edge.node ? [...acc, edge.node] : acc),
      [],
    );
    return (
      <div className={className} css={tabsContainer}>
        {navLinkInfos.map((navLinkInfo) => {
          const headingId = `${id}-${navLinkInfo.id}`;

          return (
            <section
              aria-labelledby={headingId}
              key={navLinkInfo.id}
              id={navLinkInfo.id}
              ref={navLinkInfo.sectionRef}
              css={
                activeSectionId === navLinkInfo.id
                  ? tabContainerActive
                  : tabContainerInactive
              }
            >
              <h2 css={invisible} id={headingId}>
                {navLinkInfo.text}
              </h2>

              {match(navLinkInfo.id)
                .with("additional-information", () => (
                  <AppAdditionalInfo
                    aria-labelledby={navLinkInfo.text}
                    infos={infos}
                    version={currentPlatformVersion}
                  />
                ))
                .with("faq", () => (
                  <AppFaqs aria-labelledby={navLinkInfo.text} faqs={faqs} />
                ))
                .with("how-to-use", () => (
                  <AppHowToUse
                    aria-labelledby={navLinkInfo.text}
                    guides={guides}
                    tutorials={tutorials}
                  />
                ))
                .with("ratings-and-reviews", () =>
                  currentPlatformVersion ? (
                    <AppRatingAndReviews
                      aria-labelledby={navLinkInfo.text}
                      version={currentPlatformVersion}
                    />
                  ) : (
                    <></>
                  ),
                )
                .with("team-analysis", () => (
                  <AppTeamAnalysis
                    aria-labelledby={navLinkInfo.text}
                    teamAnalysis={teamAnalysis}
                  />
                ))
                .otherwise(() => null)}
            </section>
          );
        })}
      </div>
    );
  },
);

AppTabContent.displayName = "AppTabContent";

export default AppTabContent;
