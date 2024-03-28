import { StylableFC } from "@asl-19/react-dom-utils";
import { useRouter } from "next/router";
import { Dispatch, memo, SetStateAction, useEffect, useRef } from "react";

import AppNavLinkList from "src/components/App/AppTabContent/AppNavLinkList";
import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import PageSegment from "src/components/Page/PageSegment";
import RewardsTabContent from "src/components/RewardsPage/RewardsTabContent";
import {
  RewardsDetailsSectionId,
  rewardsDetailsSectionIds,
} from "src/components/RewardsPage/rewardsValues";
import useFocusElementAfterRender from "src/hooks/useFocusElementAfterRender";
import { tabDetailsContainer } from "src/styles/tabStyles";

const RewardsDetailsSection: StylableFC<{
  activeSectionId: RewardsDetailsSectionId;
  hasFinishedQuiz: boolean | null;
  navLinkInfos: Array<AppNavLinkInfo<RewardsDetailsSectionId>>;
  referralSlug: string;
  setActiveSectionId: Dispatch<SetStateAction<RewardsDetailsSectionId>>;
}> = memo(
  ({
    activeSectionId,
    hasFinishedQuiz,
    navLinkInfos,
    referralSlug,
    setActiveSectionId,
    ...remainingProps
  }) => {
    const router = useRouter();

    const focusElementAfterRender = useFocusElementAfterRender();

    const hasLoadedHashIdRef = useRef(false);

    // Load hash section ID into state if set, then bring associated nav item into
    // view and focus associated section (will only run once)
    useEffect(() => {
      if (hasLoadedHashIdRef.current) {
        return;
      }

      // const pathHash = window.location.hash.split("#")[1];
      const pathHash = router.asPath.split("#")[1];

      const hashSectionId = Object.values(rewardsDetailsSectionIds).includes(
        // @ts-expect-error (pathHash won’t necessarily be RewardsDetailsSectionId but
        // TypeScript reports an error if it’s not?)
        pathHash,
      )
        ? (pathHash as RewardsDetailsSectionId)
        : null;

      if (hashSectionId) {
        setActiveSectionId(hashSectionId);

        const hashNavLinkInfo = navLinkInfos.find(
          (navLinkInfo) => navLinkInfo.id === hashSectionId,
        );

        if (hashNavLinkInfo?.navItemRef.current) {
          hashNavLinkInfo.navItemRef.current.scrollIntoView({
            block: "start",
            inline: "nearest",
          });
        }

        // Focus tab section if specified in hash
        if (hashNavLinkInfo?.sectionRef.current) {
          focusElementAfterRender(hashNavLinkInfo.sectionRef.current);
        }
      }

      hasLoadedHashIdRef.current = true;
    }, [
      activeSectionId,
      focusElementAfterRender,
      navLinkInfos,
      router.asPath,
      setActiveSectionId,
    ]);

    return (
      <PageSegment
        centeredContainerCss={tabDetailsContainer}
        {...remainingProps}
      >
        <AppNavLinkList
          activeSectionId={activeSectionId}
          navLinkInfos={navLinkInfos}
          setActiveSectionId={setActiveSectionId}
        />

        <RewardsTabContent
          activeSectionId={activeSectionId}
          navLinkInfos={navLinkInfos}
          referralSlug={referralSlug}
          hasFinishedQuiz={hasFinishedQuiz}
        />
      </PageSegment>
    );
  },
);

RewardsDetailsSection.displayName = "RewardsDetailsSection";

export default RewardsDetailsSection;
