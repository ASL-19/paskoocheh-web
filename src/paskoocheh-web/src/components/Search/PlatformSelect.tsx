import { MenuButton, useMenuStore } from "@ariakit/react/menu";
import { hiddenWhenJs, hiddenWhenNoJs } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useMemo } from "react";
import { match } from "ts-pattern";

import ChevronSvg from "src/components/icons/general/ChevronSvg";
import PlatformSelectMenu from "src/components/Search/PlatformSelectMenu";
import PlatformSelectNoJsSelect from "src/components/Search/PlatformSelectNoJsSelect";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import { useAppStrings } from "src/stores/appStore";
import { useAppLocaleInfo } from "src/stores/appStore";
import { paragraphP1Regular } from "src/styles/typeStyles";
import getPlatformDisplayNames from "src/utils/getPlatformDisplayNames";
import colors from "src/values/colors";

export type PlatformSelectStrings = {
  /**
   * Menu button accessibility label, to give the user context for what the
   * select is for.
   *
   * \{platformName\} is replaced by the platform name.
   */
  a11yLabel: string;
};

export type PlatformSelectGroupInfo = {
  heading: string;
  platforms: Array<GqlPlatform>;
};

// ==============
// === Styles ===
// ==============

const borderRadius = "6.25rem";

const menuButton = css(paragraphP1Regular, {
  alignItems: "center",
  backgroundColor: colors.secondary100,
  columnGap: "0.5rem",
  display: "flex",
  height: "2.75rem",
  paddingInline: "1rem",
});

const menuButtonDesktop = css(menuButton, {
  "html.ltr &": {
    borderRadius: `${borderRadius} 0 0 ${borderRadius}`,
  },
  "html.rtl &": {
    borderRadius: `0 ${borderRadius} ${borderRadius} 0`,
  },
});

const menuButtonDesktopJs = css(menuButtonDesktop, hiddenWhenNoJs);
const menuButtonDesktopNoJs = css(menuButtonDesktop, hiddenWhenJs);

const menuButtonMobile = css(menuButton, {
  borderRadius,
});

const menuButtonMobileJs = css(menuButtonMobile, hiddenWhenNoJs);
const menuButtonMobileNoJs = css(menuButtonMobile, hiddenWhenJs);

const chevronSvg = css({
  height: "0.75rem",
  width: "0.75rem",
});

// ==============================
// ===== Next.js component ======
// ==============================
const PlatformSelect: StylableFC<{
  platforms: Array<GqlPlatform>;
  variant: "desktop" | "mobile";
}> = memo(({ platforms, variant }) => {
  const strings = useAppStrings();
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const menuStore = useMenuStore();

  const menuStoreMounted = menuStore.useState("mounted");

  const platformObject = platforms.find(
    (p) => p.name === queryOrDefaultPlatformSlug,
  );
  const platformName = platformObject
    ? getPlatformDisplayNames(platformObject, localeCode)
    : strings.shared.operatingSystemsNames.android;

  const getFilteredPlatforms = useCallback(
    (category: string) => {
      const filteredPlatforms = platforms.filter(
        (platform) => platform.category === category,
      );

      return filteredPlatforms;
    },
    [platforms],
  );

  const groupInfos = useMemo<Array<PlatformSelectGroupInfo>>(
    () => [
      {
        heading: strings.Search.mobile,
        platforms: getFilteredPlatforms("m"),
      },
      {
        heading: strings.Search.web,
        platforms: getFilteredPlatforms("w"),
      },
      {
        heading: strings.Search.desktop,
        platforms: getFilteredPlatforms("d"),
      },
    ],
    [strings, getFilteredPlatforms],
  );

  const [stylesJs, stylesNoJs] = match(variant)
    .with("desktop", () => [menuButtonDesktopJs, menuButtonDesktopNoJs])
    .with("mobile", () => [menuButtonMobileJs, menuButtonMobileNoJs])
    .exhaustive();

  return (
    <>
      <MenuButton
        aria-label={strings.PlatformSelect.a11yLabel.replace(
          "{platformName}",
          platformName,
        )}
        store={menuStore}
        css={stylesJs}
      >
        {platformName}

        <ChevronSvg css={chevronSvg} direction="down" />
      </MenuButton>

      <PlatformSelectNoJsSelect css={stylesNoJs} groupInfos={groupInfos} />

      {menuStoreMounted && (
        <PlatformSelectMenu groupInfos={groupInfos} menuStore={menuStore} />
      )}
    </>
  );
});

PlatformSelect.displayName = "PlatformSelect";

export default PlatformSelect;
