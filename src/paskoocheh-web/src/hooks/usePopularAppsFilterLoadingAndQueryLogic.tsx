import { replaceCurrentRouteWithShallowRoute } from "@asl-19/next-utils";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import { useEffect, useRef, useState } from "react";

import useAnnounceLoadingNewItemsComplete from "src/hooks/a11y/useAnnounceLoadingNewItemsComplete";
import useAnnounceLoadingNewItemsStarted from "src/hooks/a11y/useAnnounceLoadingNewItemsStarted";

/**
 * Popular apps query info.
 *
 * This is used to update popularAppsLoadingState, and is passed to
 * getVersionPreviews.
 */
export type PopularAppsQueryInfo<PageNormalizedQuery> = {
  normalizedQuery: PageNormalizedQuery;
  normalizedQueryHasChanged?: boolean;
};

/**
 * Popular Apps getPreviews function.
 */
export type PopularAppsGetPreviews<PageNormalizedQuery, Preview> = (
  queryInfo: PopularAppsQueryInfo<PageNormalizedQuery>,
) => Promise<Array<Preview>>;

/**
 * Popular apps loading state. One of these possible types:
 *
 * - `error`: Encountered an error/timeout while loading new items
 * - `loadingNew`: Loading a new set of items (because filter/ordering changed)
 * - `hasNoMore`: Has no more items to load (should NOT show load more link)
 * - `hasNone`: Has no items (should show “No items” message)
 */
export type PopularAppsLoadingState =
  | { type: "error" }
  | { type: "loadingNew" }
  | { type: "hasNone" }
  | { type: "hasNoMore" };

/**
 * Fetch and display new items when query changes.
 *
 * Takes two type parameters:
 *
 * 1. The page’s NormalizedQuery type.
 * 2. The page’s preview item type (i.e. the type set by `setPreviews`, and the
 *    type fetched by `fetchNewItems`)
 */
const usePopularAppsFilterLoadingAndQueryLogic = <
  PageNormalizedQuery extends { count: number },
  Preview extends { id: string },
>({
  getPageNormalizedQuery,
  getPreviews,
  onNewItemsLoaded,
  popularAppsInitialVersionPreviews,
}: {
  /**
   * Function that converts a Next-provided query to a normalized query.
   */
  getPageNormalizedQuery: (query: ParsedUrlQuery) => PageNormalizedQuery;

  /**
   * Function that fetches the new previews and returns an object containing:
   *
   * - `newPreviews`: Array of new preview items
   *
   *   This must match the provided `Preview` type.
   */
  getPreviews: PopularAppsGetPreviews<PageNormalizedQuery, Preview>;

  onNewItemsLoaded?: () => void;

  /**
   * Initial previews
   */
  popularAppsInitialVersionPreviews: Array<Preview>;
}) => {
  // ---------------------
  // --- Outside state ---
  // ---------------------

  const router = useRouter();

  const announceLoadingNewItemsComplete = useAnnounceLoadingNewItemsComplete();
  const announceLoadingNewItemsStarted = useAnnounceLoadingNewItemsStarted();

  // -------------
  // --- State ---
  // -------------

  const [previews, setPreviews] = useState(popularAppsInitialVersionPreviews);

  const [popularAppsLoadingState, setPopularAppsLoadingState] =
    useState<PopularAppsLoadingState>(
      popularAppsInitialVersionPreviews.length === 0
        ? { type: "hasNone" }
        : { type: "hasNoMore" },
    );

  const [queryInfo, setQueryInfo] = useState<
    PopularAppsQueryInfo<PageNormalizedQuery>
  >({
    /**
     * Normalized query.
     */
    normalizedQuery: getPageNormalizedQuery(router.query),

    normalizedQueryHasChanged: false,
  });

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
      const normalizedQuery = getPageNormalizedQuery(router.query);

      // If the query hasn’t changed don’t unnecessarily update queryInfo
      // (queryInfo is initialized based on initialNormalizedQuery).
      if (
        JSON.stringify(normalizedQuery) ===
        JSON.stringify(previousQueryInfo.normalizedQuery)
      ) {
        return previousQueryInfo;
      }

      return {
        normalizedQuery,
        normalizedQueryHasChanged: true,
      };
    });
  }, [getPageNormalizedQuery, router.query]);

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
     * function we can avoid updating previews and setPopularAppsLoadingState
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

      // Update popularAppsLoadingState based on nature of request.
      setPopularAppsLoadingState({ type: "loadingNew" });

      // The whole data fetching segment is wrapped in a try block so that if
      // there’s a network/data error we can handle it in the below catch block.
      try {
        // Note that this takes some amount of time (up to 10 seconds), during
        // which the user could trigger other requests.
        const previews = await getPreviews(queryInfo);

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

        setPreviews(() => previews);

        // Update popularAppsLoadingState
        setPopularAppsLoadingState({
          type: previews.length === 0 ? "hasNone" : "hasNoMore",
        });

        // Announce that new items have finished loading in screen reader.
        announceLoadingNewItemsComplete({
          count: previews.length,
        });
      } catch (error) {
        // If there was an error during the request display an error message.
        // The error could have been triggered by e.g. the graphQlSdk hard-coded
        // 10 second timeout, a backend failure, a frontend logic mistake, or a
        // network failure.
        //
        // We don’t bother trying to differentiate between different error
        // states here.
        console.error(error);
        setPopularAppsLoadingState({ type: "error" });
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
    getPreviews,
    onNewItemsLoaded,
    queryInfo,
  ]);

  useEffect(() => {
    if (
      queryInfo.normalizedQueryHasChanged &&
      previews[0] &&
      onNewItemsLoaded
    ) {
      onNewItemsLoaded();
    }
  }, [onNewItemsLoaded, previews, queryInfo.normalizedQueryHasChanged]);

  return {
    popularAppsLoadingState,
    previews,
    queryInfo,
  };
};

export default usePopularAppsFilterLoadingAndQueryLogic;
