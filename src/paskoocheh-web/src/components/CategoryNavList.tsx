import {
  hiddenWhenPointerCoarseOrNone,
  hiddenWhenPointerFine,
} from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useRef } from "react";

import CategoryNavListItem from "src/components/CategoryNavListItem";
import OverflowIndicatorWrapper from "src/components/OverflowIndicatorWrapper";
import { useAppStrings } from "src/stores/appStore";
import { RouteInfo } from "src/types/miscTypes";

export type CategoryNavListStrings = {
  a11yLabel: string;
};

const list = css({
  display: "flex",
  gap: "0.5rem",
  overflowX: "auto",
  paddingBlock: "0.5rem",
  width: "100%",
});

const pointerCoarseOverflowIndicatorWrapper = hiddenWhenPointerFine;

const pointerCoarseList = css(list, {
  "::-webkit-scrollbar": {
    display: "none",
  },
});

const pointerFineList = css(list, hiddenWhenPointerCoarseOrNone, {
  flexWrap: "wrap",
});

const CategoryNavList: StylableFC<{
  activeUrlComparisonQueryKeys: Array<string>;
  routeInfos: Array<RouteInfo>;
  shallow?: boolean;
}> = memo(
  ({
    activeUrlComparisonQueryKeys,
    routeInfos,
    shallow,
    ...remainingProps
  }) => {
    const strings = useAppStrings();

    const pointerCoarseListElementRef = useRef<HTMLUListElement>(null);

    const listNavListItems = routeInfos.map((routeInfo) => (
      <CategoryNavListItem
        activeUrlComparisonQueryKeys={activeUrlComparisonQueryKeys}
        key={routeInfo.name}
        listElementRef={pointerCoarseListElementRef}
        routeInfo={routeInfo}
        shallow={shallow}
      />
    ));

    return (
      <nav aria-label={strings.CategoryNavList.a11yLabel}>
        <OverflowIndicatorWrapper
          css={pointerCoarseOverflowIndicatorWrapper}
          {...remainingProps}
        >
          <ul css={pointerCoarseList} ref={pointerCoarseListElementRef}>
            {listNavListItems}
          </ul>
        </OverflowIndicatorWrapper>

        <ul css={pointerFineList}>{listNavListItems}</ul>
      </nav>
    );
  },
);

CategoryNavList.displayName = "CategoryNavList";

export default CategoryNavList;
