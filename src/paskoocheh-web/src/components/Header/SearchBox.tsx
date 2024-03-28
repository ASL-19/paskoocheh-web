import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useEffect, useState } from "react";

import DesktopSearch from "src/components/Search/DesktopSearch";
import MobileSearch from "src/components/Search/MobileSearch";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import { isValidVersionPreview, ValidVersionPreview } from "src/types/appTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import { breakpointStyles, Media } from "src/utils/media/media";

export type SearchStrings = {
  desktop: string;
  inputPlaceholder: string;
  mobile: string;
  submitButtonAriaLabel: string;
  web: string;
};

const searchBox = css(
  {
    flexGrow: "1",
    height: "2.75rem",
    marginInlineEnd: "3.4375rem",
    marginInlineStart: "1.5rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        marginInlineEnd: "0.625rem",
      },
    },
  }),
);

// ==============================
// ===== Next.js component ======
// ==============================
const SearchBox: StylableFC<{
  platforms: Array<GqlPlatform>;
}> = memo(({ platforms, ...remainingProps }) => {
  const platformSlug = useQueryOrDefaultPlatformSlug();

  const [versionPreviews, setVersionPreviews] = useState<
    Array<ValidVersionPreview>
  >([]);

  useEffect(() => {
    (async () => {
      const graphQlSdk = await getGraphQlSdk();

      const appPreviewResponse = await graphQlSdk.getVersionPreviews({
        first: 99,
        orderBy: "last_modified",
        platformSlug,
      });
      const versionPreviews = (appPreviewResponse.versions?.edges || []).reduce(
        (acc, edge) =>
          isValidVersionPreview(edge.node) ? [...acc, edge.node] : acc,
        [],
      );

      setVersionPreviews(versionPreviews);
    })();
  }, [platformSlug]);

  return (
    <>
      <Media greaterThanOrEqual="singleColumn">
        <DesktopSearch
          platforms={platforms}
          versionPreviews={versionPreviews}
          css={searchBox}
          {...remainingProps}
        />
      </Media>

      <Media lessThan="singleColumn">
        <MobileSearch
          platforms={platforms}
          versionPreviews={versionPreviews}
          css={searchBox}
          {...remainingProps}
        />
      </Media>
    </>
  );
});

SearchBox.displayName = "SearchBox";

export default SearchBox;
