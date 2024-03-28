import { useDialogStore } from "@ariakit/react/dialog";
import { useMenuStore } from "@ariakit/react/menu";
import { hiddenWhenNoJs } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { memo, useCallback, useMemo } from "react";

import HeaderLogo from "src/components/Header/HeaderLogo";
import HeaderNavLinkList from "src/components/Header/HeaderNavLinkList";
import { HeaderNavLinkListItemLinkInfo } from "src/components/Header/HeaderNavLinkListItem";
import MobileHeaderNavDropdown from "src/components/Header/MobileHeaderNavDropdown";
import MobileHeaderNavMenuButton from "src/components/Header/MobileHeaderNavMenuButton";
import SearchBox from "src/components/Header/SearchBox";
import LogoutSvg from "src/components/icons/general/LogoutSvg";
import RewardSvg from "src/components/icons/general/RewardSvg";
import UserSvg from "src/components/icons/general/UserSvg";
import PageSegment from "src/components/Page/PageSegment";
import PopoverMenu from "src/components/PopoverMenu";
import { MenuItemInfo } from "src/components/PopoverMenuItem";
import { GqlPlatform } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import {
  useAppDispatch,
  useAppLocaleInfo,
  useAppStrings,
  useAppUsername,
} from "src/stores/appStore";
import removeRefreshToken from "src/utils/api/removeRefreshToken";
import { Media } from "src/utils/media/media";
import { headerHeight } from "src/values/layoutValues";
import zIndexes from "src/values/zIndexes";

export type HeaderStrings = {
  /**
   * Label for user icon when user is signed in. When clicked will open the user
   * menu.
   */
  userMenuLabel: string;
};

const pageSegmentCenteredContainer = css({
  alignItems: "center",
  display: "flex",
  height: headerHeight,
  justifyContent: "space-between",
  paddingBlock: "0.625rem",
  zIndex: zIndexes.Header_centeredContainer,
});

const shrinkingContainer = css({
  display: "flex",
  flex: "1 0 auto",
});

const headerNavigationContainer = css({
  alignItems: "center",
  columnGap: "1.5rem",
  display: "flex",
});

const headerNavContainer = css(shrinkingContainer);

const Header: StylableFC<{
  platforms: Array<GqlPlatform> | null;
}> = memo(({ className, platforms }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const router = useRouter();

  const user = useAppUsername();
  const appDispatch = useAppDispatch();

  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const mobileHeaderNavDialogStore = useDialogStore();
  const mobileHeaderNavDialogIsMounted =
    mobileHeaderNavDialogStore.useState("mounted");

  const userMenuStore = useMenuStore({ placement: "bottom-end" });

  const userMenuStoreIsMounted = userMenuStore.useState("mounted");

  const onLogoutClick = useCallback(() => {
    appDispatch({ type: "usernameChanged", username: null });
    removeRefreshToken();
    mobileHeaderNavDialogStore.hide();
  }, [appDispatch, mobileHeaderNavDialogStore]);

  const encodedPath = encodeURIComponent(router.asPath);

  const navLinkInfos = useMemo<Array<HeaderNavLinkListItemLinkInfo>>(
    () => [
      {
        href: routeUrls.home({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.app,
      },
      {
        href: routeUrls.blog({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.blog,
      },
      {
        href: routeUrls.about({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.about,
      },
      {
        href: routeUrls.rewards({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        IconComponent: RewardSvg,
        label: strings.shared.navLinks.rewards,
      },
      ...(user
        ? [
            {
              IconComponent: UserSvg,
              label: strings.Header.userMenuLabel,
              menuStore: userMenuStore,
            },
          ]
        : [
            {
              href: routeUrls.signIn({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
                returnPath: encodedPath,
              }),
              IconComponent: UserSvg,
              label: strings.shared.navLinks.account.signInOrRegister,
            },
          ]),
    ],
    [
      encodedPath,
      localeCode,
      queryOrDefaultPlatformSlug,
      strings,
      user,
      userMenuStore,
    ],
  );

  const mobileNavLinkInfos = useMemo<Array<HeaderNavLinkListItemLinkInfo>>(
    () => [
      {
        href: routeUrls.about({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.about,
      },
      {
        href: routeUrls.blog({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.blog,
      },
      ...(user
        ? [
            {
              href: routeUrls.rewards({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
              }),
              text: strings.shared.navLinks.rewards,
            },
            {
              href: routeUrls.account({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
              }),
              text: strings.shared.navLinks.account.accountSettings,
            },

            {
              onClick: onLogoutClick,
              text: strings.shared.navLinks.account.logOut,
            },
          ]
        : [
            {
              href: routeUrls.signIn({
                localeCode,
                platform: queryOrDefaultPlatformSlug,
                returnPath: encodedPath,
              }),
              text: strings.shared.navLinks.account.signInOrRegister,
            },
          ]),
    ],
    [
      encodedPath,
      localeCode,
      onLogoutClick,
      queryOrDefaultPlatformSlug,
      strings,
      user,
    ],
  );

  const headerMenuListItemInfos = useMemo<Array<MenuItemInfo>>(
    () => [
      {
        href: routeUrls.account({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
        text: strings.shared.navLinks.account.accountSettings,
      },
      {
        IconComponent: LogoutSvg,
        onClick: onLogoutClick,
        text: strings.shared.navLinks.account.logOut,
      },
    ],
    [localeCode, onLogoutClick, queryOrDefaultPlatformSlug, strings],
  );

  return (
    <PageSegment
      as="header"
      centeredContainerCss={pageSegmentCenteredContainer}
    >
      <HeaderLogo />

      {platforms && <SearchBox platforms={platforms} />}

      <div css={headerNavigationContainer}>
        <Media lessThan="desktopNarrow">
          <MobileHeaderNavMenuButton
            className={className}
            css={hiddenWhenNoJs}
            dialogStore={mobileHeaderNavDialogStore}
          />

          {mobileHeaderNavDialogIsMounted && (
            <MobileHeaderNavDropdown
              navLinkInfos={mobileNavLinkInfos}
              dialogStore={mobileHeaderNavDialogStore}
            />
          )}
        </Media>

        <Media greaterThanOrEqual="desktopNarrow">
          <div css={headerNavContainer}>
            <HeaderNavLinkList navLinkInfos={navLinkInfos} isMobile={false} />

            {userMenuStoreIsMounted && (
              <PopoverMenu
                menuItemInfos={headerMenuListItemInfos}
                menuStore={userMenuStore}
              />
            )}
          </div>
        </Media>
      </div>
    </PageSegment>
  );
});

Header.displayName = "Header";

export default Header;
