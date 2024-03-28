import { replaceCurrentRouteWithShallowRoute } from "@asl-19/next-utils";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import { useEffect, useRef, useState } from "react";

import useAnnounceLoadingNewItemsComplete from "src/hooks/a11y/useAnnounceLoadingNewItemsComplete";
import useAnnounceLoadingNewItemsStarted from "src/hooks/a11y/useAnnounceLoadingNewItemsStarted";
import { useAppLocaleInfo } from "src/stores/appStore";
import focusElement from "src/utils/focus/focusElement";
import { LocaleCode } from "src/values/localeValues";

/**
 * Index page query info.
 *
 * This is used to update indexPageLoadingState, and is passed to
 * getPreviewsAndHasNextPage.
 */
export type IndexPageQueryInfo<PageNormalizedQuery> = {
  isLoadMoreQuery: boolean;
  localeCode: LocaleCode;
  normalizedQuery: PageNormalizedQuery;
  normalizedQueryHasChanged?: boolean;
};

/**
 * Index page getPreviewsAndHasNextPage function.
 */
export type IndexPageGetPreviewsAndHasNextPage<PageNormalizedQuery, Preview> = (
  queryInfo: IndexPageQueryInfo<PageNormalizedQuery>,
) => Promise<{
  filteredHashtag: string | null;
  hasNextPage: boolean;
  previews: Array<Preview>;
}>;

/**
 * Index page loading state. One of these possible types:
 *
 * - `error`: Encountered an error/timeout while loading new items
 * - `loadingNew`: Loading a new set of items (because filter/ordering changed)
 * - `loadingMore`: Loading more of the current set of items
 * - `hasMore`: Has more items to load (should show “Load more” link)
 * - `hasNoMore`: Has no more items to load (should NOT show load more link)
 * - `hasNone`: Has no items (should show “No items” message)
 */
export type IndexPageLoadingState =
  | { type: "error" }
  | { type: "loadingNew" }
  | { type: "loadingMore" }
  | { type: "hasMore" }
  | { type: "hasNoMore" }
  | { type: "hasNone" };

/**
 * Fetch and display new items when query changes.
 *
 * Takes two type parameters:
 *
 * 1. The page’s NormalizedQuery type.
 * 2. The page’s preview item type (i.e. the type set by `setPreviews`, and the
 *    type fetched by `fetchNewItems`)
 */
const useIndexPageLoadingAndQueryLogic = <
  PageNormalizedQuery extends { count: number },
  Preview extends { id: string },
>({
  getPageNormalizedQuery,
  getPreviewElementId,
  getPreviewsAndHasNextPage,
  initialFilteredHashtag,
  initialHasNextPage,
  initialPreviews,
}: {
  /**
   * Function that converts a Next-provided query to a normalized query.
   */
  getPageNormalizedQuery: (query: ParsedUrlQuery) => PageNormalizedQuery;

  /**
   * Function that returns the HTML ID of a given preview item.
   *
   * This is used to focus the first new item after more items are loaded.
   */
  getPreviewElementId: (preview: Preview) => string;

  /**
   * Function that fetches the new previews and returns an object containing:
   *
   * - `hasNextPage`: Did the query response indicate that there’s another page
   *   of results?
   *
   *   This will probably look like `!!response.items?.pageInfo.hasNextPage`
   *
   * - `newPreviews`: Array of new preview items
   *
   *   This must match the provided `Preview` type.
   */
  getPreviewsAndHasNextPage: IndexPageGetPreviewsAndHasNextPage<
    PageNormalizedQuery,
    Preview
  >;

  /**
   * Is there a filtered hashtag (only used in PostsPage)
   */
  initialFilteredHashtag: string | null;

  /**
   * Did the query response indicate that there’s another page of results?
   */
  initialHasNextPage: boolean;

  /**
   * Initial previews
   */
  initialPreviews: Array<Preview>;
}) => {
  // ---------------------
  // --- Outside state ---
  // ---------------------

  const router = useRouter();

  const announceLoadingNewItemsComplete = useAnnounceLoadingNewItemsComplete();
  const announceLoadingNewItemsStarted = useAnnounceLoadingNewItemsStarted();

  const { localeCode } = useAppLocaleInfo();

  // -------------
  // --- State ---
  // -------------

  // The text of the current filtered hashtag (used in PostsPage)
  const [filteredHashtag, setFilteredHashtag] = useState<string | null>(
    initialFilteredHashtag,
  );

  const [previews, setPreviews] = useState(initialPreviews);

  const [indexPageLoadingState, setIndexPageLoadingState] =
    useState<IndexPageLoadingState>(
      initialPreviews.length === 0
        ? { type: "hasNone" }
        : initialHasNextPage
          ? { type: "hasMore" }
          : { type: "hasNoMore" },
    );

  const [queryInfo, setQueryInfo] = useState<
    IndexPageQueryInfo<PageNormalizedQuery>
  >({
    /**
     * Is query loading more items (IndexPageLoadingState.loadingMore), or
     * loading new items (IndexPageLoadingState.loadingNew)?
     */
    isLoadMoreQuery: false,

    /**
     * Locale code of query.
     */
    localeCode,

    /**
     * Normalized query.
     */
    normalizedQuery: getPageNormalizedQuery(router.query),

    normalizedQueryHasChanged: false,
  });

  const [focusElementId, setFocusElementId] = useState<string | null>(null);

  // ------------------------------------------------------
  // --- Replace the initial route with a shallow route ---
  // ------------------------------------------------------

  // If we didn’t replace the initial route Next.js would do an unnecessary
  // full page load (running getServerSideProps and displaying the global
  // loading indicator rather than the page-specific loading indicator) if
  // the user navigated back to the initial ProfilesPage route via the back
  // button/gesture
  //
  // See replaceCurrentRouteWithShallowRoute for more details.

  const hasReplacedInitialRouteWithShallowRoute = useRef(false);

  useEffect(() => {
    if (
      !queryInfo.normalizedQueryHasChanged &&
      !hasReplacedInitialRouteWithShallowRoute.current
    ) {
      hasReplacedInitialRouteWithShallowRoute.current = true;

      replaceCurrentRouteWithShallowRoute({ router });
    }
  }, [queryInfo.normalizedQueryHasChanged, router]);

  // -----------------------------------------------
  // --- Update queryInfo on router.query change ---
  // -----------------------------------------------

  useEffect(() => {
    setQueryInfo((previousQueryInfo) => {
      const previousNormalizedQuery = previousQueryInfo.normalizedQuery;

      const normalizedQuery = getPageNormalizedQuery(router.query);

      // If the query hasn’t changed don’t unnecessarily update queryInfo
      // (queryInfo is initialized based on initialNormalizedQuery).
      if (
        JSON.stringify(normalizedQuery) ===
        JSON.stringify(previousQueryInfo.normalizedQuery)
      ) {
        return previousQueryInfo;
      }

      // The query is loading more if the query’s filter properties are the same
      // as the previous query’s filter properties, and the query’s count property is
      // higher than the previous query’s count property
      const isLoadMoreQuery = Object.keys(normalizedQuery).every((queryKey) =>
        queryKey === "count"
          ? normalizedQuery.count > previousNormalizedQuery.count
          : normalizedQuery[queryKey] === previousNormalizedQuery[queryKey],
      );

      return {
        isLoadMoreQuery,
        localeCode,
        normalizedQuery,
        normalizedQueryHasChanged: true,
      };
    });
  }, [getPageNormalizedQuery, localeCode, router.query]);

  // ----------------------------------------------------------
  // --- Fetch and display new items when queryInfo changes ---
  // ----------------------------------------------------------

  useEffect(() => {
    // Don’t perform any data fetching if the normalized query hasn’t changed
    // since initial render.
    if (!queryInfo.normalizedQueryHasChanged) {
      return;
    }

    /**
     * Is this an outdated request?
     *
     * @remarks
     * The code inside this useEffect block runs each time queryInfo is changed;
     * the [cleanup] function returned at the bottom of this block runs right
     * before this useEffect is triggered again, AND right before the component
     * unmounts (when the user leaves the page).
     *
     * By initializing this to false and setting it to true in the cleanup
     * function we can avoid updating previews and setIndexPageLoadingState
     * based on the result of an outdated request triggered by a previous
     * useEffect run.
     *
     * If the user is still on this page acting on the outdated response could
     * cause confusing/outdated page updates; if the user has left the page the
     * attempted update would cause the React “Can't perform a React state
     * update on an unmounted component” warning.
     *
     * [cleanup]:
     * https://reactjs.org/docs/hooks-effect.html#effects-without-cleanup
     * [closure]:
     * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures
     */
    let shouldIgnoreResponse = false;

    (async () => {
      // Announce that new items have started loading in screen reader.
      announceLoadingNewItemsStarted();

      // Update indexPageLoadingState based on nature of request.
      setIndexPageLoadingState(
        queryInfo.isLoadMoreQuery
          ? { type: "loadingMore" }
          : { type: "loadingNew" },
      );

      // The whole data fetching segment is wrapped in a try block so that if
      // there’s a network/data error we can handle it in the below catch block.
      try {
        // Note that this takes some amount of time (up to 10 seconds), during
        // which the user could trigger other requests.
        const { filteredHashtag, hasNextPage, previews } =
          await getPreviewsAndHasNextPage(queryInfo);

        // Bail out early if this request is outdated.
        //
        // If the user has triggered another request (by clicking another filter
        // link or navigating via browser history) while this request was
        // loading there’s no point in applying this result; in fact doing so
        // could lead to incorrect data being displayed since API responses
        // don’t necessarily arrive in the order they were requested.
        if (shouldIgnoreResponse) {
          return;
        }

        // Update current filtered hashtag (this is only used in PostsPage)
        setFilteredHashtag(filteredHashtag);

        // If this is a load more query the new value is the previous values +
        // the new values (with existing values filtered out). There shouldn’t
        // usually be duplicate values but it could happen if e.g. the editors
        // added or removed profiles between the previous and current request.
        setPreviews((previousPreviews) =>
          queryInfo.isLoadMoreQuery
            ? [
                ...previousPreviews,
                ...previews.filter(
                  (newPreview) =>
                    !previousPreviews.some(
                      (previousPreview) => newPreview.id === previousPreview.id,
                    ),
                ),
              ]
            : previews,
        );

        // Update indexPageLoadingState
        setIndexPageLoadingState(
          // If this isn’t a “load more” request and the response contains no
          // items then there are no items (we don’t want all of the existing
          // items hidden from the user if just the “load more” query doesn’t
          // have any items).
          //
          // Otherwise we set indexPageLoadingState to hasMore or hasNoMore
          // depending on the value of hasNextPage
          !queryInfo.isLoadMoreQuery && previews.length === 0
            ? { type: "hasNone" }
            : hasNextPage
              ? { type: "hasMore" }
              : { type: "hasNoMore" },
        );

        // Announce that new items have finished loading in screen reader.
        announceLoadingNewItemsComplete({
          count: previews.length,
        });

        // If ths is a “load more” query we focus the first new item. It’s
        // important to focus something since the user’s previous focus was on
        // the “load more” link, which disappeared during loading. This also
        // feels like the most natural thing to do with the user’s focus since
        // it follows their intent to load more items.
        if (queryInfo.isLoadMoreQuery && previews[0]) {
          setFocusElementId(getPreviewElementId(previews[0]));
        }
      } catch (error) {
        // If there was an error during the request display an error message.
        // The error could have been triggered by e.g. the graphQlSdk hard-coded
        // 10 second timeout, a backend failure, a frontend logic mistake, or a
        // network failure.
        //
        // We don’t bother trying to differentiate between different error
        // states here.
        console.error(error);
        setIndexPageLoadingState({ type: "error" });
      }
    })();

    // Cleanup function: mark this request to avoid state updates based on the
    // response of an outdated request.
    return () => {
      shouldIgnoreResponse = true;
    };
  }, [
    announceLoadingNewItemsComplete,
    announceLoadingNewItemsStarted,
    getPreviewElementId,
    getPreviewsAndHasNextPage,
    queryInfo,
  ]);

  // -----------------------------------------
  // --- Focus focusElementId when updated ---
  // -----------------------------------------
  useEffect(() => {
    if (focusElementId) {
      focusElement(document.getElementById(focusElementId), {
        preventScroll: true,
      });
    }
  }, [focusElementId]);

  return {
    filteredHashtag,
    indexPageLoadingState,
    previews,
    queryInfo,
  };
};

export default useIndexPageLoadingAndQueryLogic;
