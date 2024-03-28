import { invisible } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import {
  memo,
  MouseEventHandler,
  useCallback,
  useEffect,
  useId,
  useRef,
} from "react";

import SearchSvg from "src/components/icons/general/SearchSvg";
import PlatformSelect from "src/components/Search/PlatformSelect";
import SearchInput from "src/components/Search/SearchInput";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import useSearchFormOnSubmit from "src/hooks/useSearchFormOnSubmit";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { ValidVersionPreview } from "src/types/appTypes";
import colors from "src/values/colors";

// ==============
// === Styles ===
// ==============
const formContainer = css({
  display: "flex",
});

const container = css({
  display: "flex",
  flex: "1 1 auto",
  justifyContent: "space-between",
  position: "relative",
});

const searchLink = css({
  display: "flex",
});

const searchLinkIcon = css({
  alignSelf: "center",
  color: colors.shadesBlack,
  display: "flex",
  height: "1.5rem",
  width: "1.5rem",
});

const searchInputBackground = css(
  {
    backgroundColor: colors.shadesWhite,
    display: "flex",
    inset: 0,
    position: "absolute",
    width: "100%",
  },
  {
    ":not(:focus-within)": invisible,
  },
);

// ==============================
// ===== Next.js component ======
// ==============================
const MobileSearch: StylableFC<{
  platforms: Array<GqlPlatform>;
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(({ platforms, versionPreviews, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();
  const strings = useAppStrings();
  const searchLinkElementRef = useRef<HTMLAnchorElement>(null);
  const comboboxInputRef = useRef<HTMLInputElement>(null);

  const comboboxInputId = useId();

  const formElementRef = useRef<HTMLFormElement>(null);

  const onButtonClick = useCallback<MouseEventHandler<HTMLAnchorElement>>(
    (event) => {
      event.preventDefault();

      comboboxInputRef.current?.focus();
    },
    [],
  );

  const handleKeyPress = useCallback((event: KeyboardEvent) => {
    if (
      event.key === "Escape" &&
      event.target instanceof HTMLElement &&
      comboboxInputRef.current?.contains(event.target)
    ) {
      searchLinkElementRef.current?.focus();
    }
  }, []);

  useEffect(() => {
    document.addEventListener("keydown", handleKeyPress);

    return () => {
      document.removeEventListener("keydown", handleKeyPress);
    };
  }, [handleKeyPress]);

  const onClearButtonClick = useCallback(() => {
    searchLinkElementRef.current?.focus();
  }, []);

  const onFormSubmit = useSearchFormOnSubmit({ formElementRef });

  return (
    <form
      action={routeUrls.searchResults({
        localeCode,
        platform: queryOrDefaultPlatformSlug,
      })}
      css={formContainer}
      onSubmit={onFormSubmit}
      ref={formElementRef}
      {...remainingProps}
    >
      <div css={container}>
        <PlatformSelect variant="mobile" platforms={platforms} />

        <a
          css={searchLink}
          onClick={onButtonClick}
          href={`#${comboboxInputId}`}
          ref={searchLinkElementRef}
          aria-label={strings.Search.inputPlaceholder}
        >
          <SearchSvg css={searchLinkIcon} />
        </a>

        {/* This container is necessary to put a rectangular white background
        across the whole area. SearchInput has a border radius so SearchSvg
        would be visible beneath it without this. */}
        <div css={searchInputBackground}>
          <SearchInput
            comboboxInputElementRef={comboboxInputRef}
            comboboxInputId={comboboxInputId}
            onClearButtonClick={onClearButtonClick}
            versionPreviews={versionPreviews}
          />
        </div>
      </div>
    </form>
  );
});

MobileSearch.displayName = "MobileSearch";

export default MobileSearch;
