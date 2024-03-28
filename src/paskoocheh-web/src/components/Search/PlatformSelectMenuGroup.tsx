import { MenuGroup, MenuGroupLabel } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { memo } from "react";

import MenuItemLink from "src/components/MenuItemLink";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import { useAppLocaleInfo } from "src/stores/appStore";
import { dropdownBackgroundWhenActiveItem } from "src/styles/dropdownStyles";
import { paragraphP1Regular, paragraphP2SemiBold } from "src/styles/typeStyles";
import getPlatformDisplayNames from "src/utils/getPlatformDisplayNames";
import colors from "src/values/colors";

const list = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "0.75rem",
});

const item = css({
  // Give padding so link active/hover state (dropdownBackgroundWhenActiveItem)
  // looks better, and reverse layout effect with negative margin.
  margin: "-0.25rem",
  padding: "0.25rem",
});

const label = css(paragraphP2SemiBold, item);

const link = css(paragraphP1Regular, item, dropdownBackgroundWhenActiveItem, {
  color: colors.secondary400,
  cursor: "pointer",
});

const PlatformSelectMenuGroup: StylableFC<{
  heading: string;
  platforms: Array<GqlPlatform>;
}> = memo(({ heading, platforms, ...remainingProps }) => {
  const router = useRouter();
  const { localeCode } = useAppLocaleInfo();
  const queryPlatform = useQueryOrDefaultPlatformSlug();

  return (
    <MenuGroup css={list} {...remainingProps}>
      <MenuGroupLabel css={label}>{heading}</MenuGroupLabel>

      {platforms &&
        platforms.map((platform, index) => {
          const currentHref = router.asPath;
          const urlPlatformSlug = platform.slugName;

          // Note: this works in conjunction with
          // useFocusMainHeadingOnRouteChange’s newUrlOnlyChangedPlatform to avoid
          // moving focus to the current page’s heading when these links are
          // clicked
          const href = urlPlatformSlug
            ? currentHref.replace(queryPlatform, platform.slugName)
            : currentHref;

          const displayName = getPlatformDisplayNames(platform, localeCode);

          return (
            <MenuItemLink
              content={displayName}
              href={href}
              key={index}
              css={link}
            />
          );
        })}
    </MenuGroup>
  );
});

PlatformSelectMenuGroup.displayName = "PlatformSelectMenuGroup";

export default PlatformSelectMenuGroup;
