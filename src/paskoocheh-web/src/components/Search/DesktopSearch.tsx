import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useRef } from "react";

import PlatformSelect from "src/components/Search/PlatformSelect";
import SearchInput from "src/components/Search/SearchInput";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import useSearchFormOnSubmit from "src/hooks/useSearchFormOnSubmit";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import { ValidVersionPreview } from "src/types/appTypes";

// ==============
// === Styles ===
// ==============
const container = css({
  display: "flex",
});

// ==============================
// ===== Next.js component ======
// ==============================

const DesktopSearch: StylableFC<{
  platforms: Array<GqlPlatform>;
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(({ platforms, versionPreviews, ...props }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const formElementRef = useRef<HTMLFormElement>(null);

  const onFormSubmit = useSearchFormOnSubmit({ formElementRef });

  return (
    <form
      action={routeUrls.searchResults({
        localeCode,
        platform: queryOrDefaultPlatformSlug,
      })}
      css={container}
      onSubmit={onFormSubmit}
      ref={formElementRef}
      {...props}
    >
      <PlatformSelect variant="desktop" platforms={platforms} />

      <SearchInput
        versionPreviews={versionPreviews}
        focusComboboxInputElementOnClear
      />
    </form>
  );
});

DesktopSearch.displayName = "DesktopSearch";

export default DesktopSearch;
