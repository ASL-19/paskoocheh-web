import { useHrefIsActive } from "@asl-19/next-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { memo, RefObject, useEffect, useRef } from "react";
import scrollIntoView from "scroll-into-view-if-needed";

import { useAppLocaleInfo } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";
import { RouteInfo } from "src/types/miscTypes";
import colors from "src/values/colors";

const categoryLink = ({ isActive }: { isActive: boolean }) =>
  css(paragraphP2SemiBold, {
    backgroundColor: isActive ? colors.secondary500 : "",
    borderRadius: "2rem",
    color: isActive ? colors.shadesWhite : colors.secondary500,
    display: "block",
    height: "1.875rem",
    lineHeight: "1.875rem",
    maxWidth: "max-content",
    minWidth: "max-content",
    padding: "0 1rem",
    whiteSpace: "nowrap",
  });

const CategoryNavListItem: StylableFC<{
  activeUrlComparisonQueryKeys: Array<string>;
  listElementRef: RefObject<HTMLUListElement>;
  routeInfo: RouteInfo;
  shallow?: boolean;
}> = memo(
  ({
    activeUrlComparisonQueryKeys,
    listElementRef,
    routeInfo,
    shallow,
    ...remainingProps
  }) => {
    const { direction } = useAppLocaleInfo();

    const linkElementRef = useRef<HTMLAnchorElement>(null);

    const isActive = useHrefIsActive({
      activeUrlComparisonQueryKeys,
      href: routeInfo.route,
      webPublicUrl: process.env.NEXT_PUBLIC_WEB_URL,
    });

    // Scroll into view if active.
    //
    // We use scroll-into-view-if-needed over the native Element.scrollIntoView
    // so we can prevent the entire browser window from scrolling using its
    // `boundary` argument [1].
    //
    // If the user e.g. navigates back to an index page in which they were
    // scrolled down we want their scroll position to be retained.
    //
    // This will:
    //
    // 1. Scroll the active item into view on page load (important on mobile
    //    where if the active category is later in the list it could be active
    //    but completely outside of view, so the user might not know the a
    //    category filter is active).
    //
    // 2. Bring items into focus as they become active. So e.g. if the user
    //    clicks an item when it’s partially out of view it will fully scroll
    //    into view, and if the user navigates back/forward the newly active
    //    item will scroll into view).
    //
    // This is only enabled in RTL due to a bug in compute-scroll-into-view:
    //
    // - https://github.com/scroll-into-view/compute-scroll-into-view/issues/821
    // - https://github.com/scroll-into-view/scroll-into-view-if-needed/issues/993
    //
    // [1] (https://github.com/scroll-into-view/compute-scroll-into-view#boundary)
    useEffect(() => {
      if (isActive && linkElementRef.current && direction === "ltr") {
        scrollIntoView(linkElementRef.current, {
          boundary: listElementRef.current,
        });
      }
    }, [direction, isActive, listElementRef]);

    return (
      // AFAIK we need to use legacyBehaviour to use the ref prop (Link is a
      // functional component that doesn’t use forwardRef?)
      <li>
        <Link
          href={routeInfo.route}
          legacyBehavior
          passHref
          shallow={shallow}
          {...remainingProps}
        >
          {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
          <a css={categoryLink({ isActive })} ref={linkElementRef}>
            {routeInfo.name}
          </a>
        </Link>
      </li>
    );
  },
);

CategoryNavListItem.displayName = "CategoryNavListItem";

export default CategoryNavListItem;
