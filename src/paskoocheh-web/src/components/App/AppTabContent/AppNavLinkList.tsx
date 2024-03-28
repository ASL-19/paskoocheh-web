import {
  hiddenWhenPointerCoarseOrNone,
  hiddenWhenPointerFine,
} from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { Dispatch, memo, SetStateAction } from "react";

import AppNavLinkListItem, {
  AppNavLinkInfo,
} from "src/components/App/AppTabContent/AppNavLinkListItem";
import OverflowIndicatorWrapper from "src/components/OverflowIndicatorWrapper";
import { useAppStrings } from "src/stores/appStore";

export type AppNavLinkListStrings = {
  a11yLabel: string;
};

const list = css({
  columnGap: "2rem",
  display: "flex",
  overflowX: "auto",
  overflowY: "hidden",
});

const pointerCoarseOverflowIndicatorWrapper = css(hiddenWhenPointerFine, {
  marginBlock: "-0.5rem",
  paddingBlock: "0.5rem",
});

const pointerCoarseList = css(list, {
  "::-webkit-scrollbar": {
    display: "none",
  },
});

const pointerFineList = css(list, hiddenWhenPointerCoarseOrNone, {
  flexWrap: "wrap",
});

const AppNavLinkList: StylableFC<{
  activeSectionId: string;
  navLinkInfos: Array<AppNavLinkInfo>;
  setActiveSectionId: Dispatch<SetStateAction<string>>;
}> = memo(({ activeSectionId, navLinkInfos, setActiveSectionId }) => {
  const strings = useAppStrings();

  const appNavLinkListItems = navLinkInfos.map((navLinkInfo) => (
    <AppNavLinkListItem
      activeSectionId={activeSectionId}
      key={navLinkInfo.text}
      linkInfo={navLinkInfo}
      setActiveSectionId={setActiveSectionId}
    />
  ));

  return (
    <nav aria-label={strings.AppNavLinkList.a11yLabel}>
      <OverflowIndicatorWrapper css={pointerCoarseOverflowIndicatorWrapper}>
        <ul css={pointerCoarseList}>{appNavLinkListItems}</ul>
      </OverflowIndicatorWrapper>

      <ul css={pointerFineList}>{appNavLinkListItems}</ul>
    </nav>
  );
});

AppNavLinkList.displayName = "AppNavLinkList";

export default AppNavLinkList;
