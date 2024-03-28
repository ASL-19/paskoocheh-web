import { invisible } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, useId } from "react";
import { match } from "ts-pattern";

import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import RewardsDashboard from "src/components/RewardsPage/RewardsDashboard/RewardsDashboard";
import RewardsRedemption from "src/components/RewardsPage/RewardsRedemption/RewardsRedemption";
import RewardsReview from "src/components/RewardsPage/RewardsReview/RewardsReview";
import { RewardsDetailsSectionId } from "src/components/RewardsPage/rewardsValues";
import {
  tabContainerActive,
  tabContainerInactive,
  tabsContainer,
} from "src/styles/tabStyles";

const RewardsTabContent: StylableFC<{
  activeSectionId: RewardsDetailsSectionId;
  hasFinishedQuiz: boolean | null;
  navLinkInfos: Array<AppNavLinkInfo<RewardsDetailsSectionId>>;
  referralSlug: string;
}> = memo(
  ({
    activeSectionId,
    className,
    hasFinishedQuiz,
    navLinkInfos,
    referralSlug,
  }) => {
    const id = useId();

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
                .with("dashboard", () => (
                  <RewardsDashboard
                    aria-labelledby={navLinkInfo.text}
                    referralSlug={referralSlug}
                    hasFinishedQuiz={hasFinishedQuiz}
                  />
                ))
                .with("my-review", () => (
                  <RewardsReview aria-labelledby={navLinkInfo.text} />
                ))

                .with("redemption", () => (
                  <RewardsRedemption aria-labelledby={navLinkInfo.text} />
                ))

                .otherwise(() => null)}
            </section>
          );
        })}
      </div>
    );
  },
);

RewardsTabContent.displayName = "RewardsTabContent";

export default RewardsTabContent;
