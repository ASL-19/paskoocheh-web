import { StylableFC } from "@asl-19/react-dom-utils";
import { useRouter } from "next/router";
import { memo, useEffect, useMemo, useRef, useState } from "react";

import AppNavLinkList from "src/components/App/AppTabContent/AppNavLinkList";
import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import AppTabContent from "src/components/App/AppTabContent/AppTabContent";
import {
  AppDetailsSectionId,
  appDetailsSectionIds,
} from "src/components/App/appValues";
import PageSegment from "src/components/Page/PageSegment";
import { GqlInfo } from "src/generated/graphQl";
import useFocusElementAfterRender from "src/hooks/useFocusElementAfterRender";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { tabDetailsContainer } from "src/styles/tabStyles";
import { ValidVersion } from "src/types/appTypes";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";

export type AppDetailsSectionStrings = {
  headings: {
    additionalInfo: string;
    faq: string;
    howToUse: string;
    ratingsAndReviews: string;
    teamAnalysis: string;
  };
};

const AppDetailsSection: StylableFC<{
  currentPlatformVersion: ValidVersion;
  infos: Array<GqlInfo>;
}> = memo(({ currentPlatformVersion, infos, ...remainingProps }) => {
  const router = useRouter();

  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const focusElementAfterRender = useFocusElementAfterRender();

  const teamAnalysisSectionRef = useRef<HTMLDivElement>(null);
  const ratingsAndReviewsSectionRef = useRef<HTMLDivElement>(null);
  const additionalInformationSectionRef = useRef<HTMLDivElement>(null);
  const faqSectionRef = useRef<HTMLDivElement>(null);
  const howToUseSectionRef = useRef<HTMLDivElement>(null);

  const teamAnalysisNavItemRef = useRef<HTMLLIElement>(null);
  const ratingsAndReviewsNavItemRef = useRef<HTMLLIElement>(null);
  const additionalInformationNavItemRef = useRef<HTMLLIElement>(null);
  const faqNavItemRef = useRef<HTMLLIElement>(null);
  const howToUseNavItemRef = useRef<HTMLLIElement>(null);

  const navLinkInfos = useMemo<
    [
      AppNavLinkInfo<AppDetailsSectionId>,
      ...Array<AppNavLinkInfo<AppDetailsSectionId>>,
    ]
  >(() => {
    const appUrl = routeUrls.app({
      localeCode,
      platform: queryOrDefaultPlatformSlug,
      slug: currentPlatformVersion.tool.slug,
      toolType: getValidToolPrimaryToolType(currentPlatformVersion.tool).slug,
    });

    return [
      {
        id: appDetailsSectionIds.teamAnalysis,
        navItemRef: teamAnalysisNavItemRef,
        sectionRef: teamAnalysisSectionRef,
        text: strings.AppDetailsSection.headings.teamAnalysis,
        url: `${appUrl}#${appDetailsSectionIds.teamAnalysis}`,
      },
      {
        id: appDetailsSectionIds.ratingsAndReviews,
        navItemRef: ratingsAndReviewsNavItemRef,
        sectionRef: ratingsAndReviewsSectionRef,
        text: strings.AppDetailsSection.headings.ratingsAndReviews,
        url: `${appUrl}#${appDetailsSectionIds.ratingsAndReviews}`,
      },
      {
        id: appDetailsSectionIds.additionalInfo,
        navItemRef: additionalInformationNavItemRef,
        sectionRef: additionalInformationSectionRef,
        text: strings.AppDetailsSection.headings.additionalInfo,
        url: `${appUrl}#${appDetailsSectionIds.additionalInfo}`,
      },
      {
        id: appDetailsSectionIds.faq,
        navItemRef: faqNavItemRef,
        sectionRef: faqSectionRef,
        text: strings.AppDetailsSection.headings.faq,
        url: `${appUrl}#${appDetailsSectionIds.faq}`,
      },
      {
        id: appDetailsSectionIds.howToUse,
        navItemRef: howToUseNavItemRef,
        sectionRef: howToUseSectionRef,
        text: strings.AppDetailsSection.headings.howToUse,
        url: `${appUrl}#${appDetailsSectionIds.howToUse}`,
      },
    ];
  }, [currentPlatformVersion, localeCode, queryOrDefaultPlatformSlug, strings]);

  const [activeSectionId, setActiveSectionId] = useState(navLinkInfos[0].id);
  const hasLoadedHashIdRef = useRef(false);

  // Load hash section ID into state if set, then bring associated nav item into
  // view and focus associated section (will only run once)
  useEffect(() => {
    if (hasLoadedHashIdRef.current) {
      return;
    }

    // const pathHash = window.location.hash.split("#")[1];
    const pathHash = router.asPath.split("#")[1];

    const hashSectionId = Object.values(appDetailsSectionIds).includes(
      // @ts-expect-error (pathHash won’t necessarily be AppDetailsSectionId but
      // TypeScript reports an error if it’s not?)
      pathHash,
    )
      ? (pathHash as AppDetailsSectionId)
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
  }, [activeSectionId, focusElementAfterRender, navLinkInfos, router.asPath]);

  return (
    <PageSegment centeredContainerCss={tabDetailsContainer} {...remainingProps}>
      <AppNavLinkList
        activeSectionId={activeSectionId}
        navLinkInfos={navLinkInfos}
        setActiveSectionId={setActiveSectionId}
      />
      <AppTabContent
        activeSectionId={activeSectionId}
        navLinkInfos={navLinkInfos}
        infos={infos}
        currentPlatformVersion={currentPlatformVersion}
      />
    </PageSegment>
  );
});

AppDetailsSection.displayName = "AppDetailsSection";

export default AppDetailsSection;
