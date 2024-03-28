import { getAbsoluteUrl } from "@asl-19/js-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import {
  memo,
  MouseEventHandler,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import DrawerDialogAndDisclosure from "src/components/DrawerDialog/DrawerDialogAndDisclosure";
import DrawerDialogLinksContent from "src/components/DrawerDialog/DrawerDialogLinksContent";
import ShareSvg from "src/components/icons/general/ShareSvg";
import SupportSvg from "src/components/icons/general/SupportSvg";
import SocialMediaShareLinkList from "src/components/SocialMediaShareLinkList";
import { GqlTool } from "src/generated/graphQl";
import useAnimatedDialogStore from "src/hooks/useAnimatedDialogState";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { RouteInfo } from "src/types/miscTypes";
import { breakpointStyles, Media } from "src/utils/media/media";
import colors from "src/values/colors";

export type AppShareAndSupportLinksStrings = {
  shareDialogA11yHeading: string;
  supportDialogHeading: string;
};

const container = css({
  alignItems: "flex-start",
  display: "flex",
  flex: "1",
  gap: "1rem",
  justifyContent: "flex-end",
  order: "2",
});

const iconSvg = css({
  width: "1.5rem",
});

const socialShareContainer = css({
  display: "flex",
  justifyContent: "center",
  padding: "2rem 0",
});

const socialMediaShareLinkListServiceItem = breakpointStyles({
  tablet: {
    lt: {
      display: "none",
    },
  },
});

const AppShareAndSupportLinks: StylableFC<{
  tool: GqlTool;
}> = memo(({ tool, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const [webShareApiIsSupported, setWebShareApiIsSupported] = useState(true);

  const shareAnimatedDialogStore = useAnimatedDialogStore();
  const supportAnimatedDialogStore = useAnimatedDialogStore();

  const supportDialogRouteInfos: Array<RouteInfo> = useMemo(
    () => [
      {
        key: "telegram-chat",
        name: "Telegram Chat",
        route: routeUrls.contact({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          // TODO: Change to toolSlug once #559 is done
          tool: tool.pk,
        }),
      },
      {
        key: "email",
        name: "Email",
        route: routeUrls.writeYourMessage({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          // TODO: Change to toolSlug once #559 is done
          tool: tool.pk,
        }),
      },
    ],
    [tool.pk, localeCode, queryOrDefaultPlatformSlug],
  );

  const absoluteUrl = getAbsoluteUrl({
    protocolAndHost: process.env.NEXT_PUBLIC_WEB_URL,
    rootRelativeUrl: routeUrls.app({
      localeCode,
      platform: queryOrDefaultPlatformSlug,
      slug: tool.slug,
      toolType:
        (tool.primaryTooltype?.slug !== "unknown"
          ? tool.primaryTooltype?.slug
          : "") || (tool.toolTypes ? tool.toolTypes[0]?.slug ?? "" : ""),
    }),
  });

  useEffect(() => {
    if (!("share" in navigator)) {
      setWebShareApiIsSupported(false);
    }
  }, []);

  const onMobileSocialMediaShareLinkListItemClick =
    useCallback<MouseEventHandler>(
      () => shareAnimatedDialogStore.hide(),
      [shareAnimatedDialogStore],
    );

  const shareDialogDisclosureContent = useMemo(
    () => <ShareSvg css={iconSvg} />,
    [],
  );

  const supportDialogDisclosureContent = useMemo(
    () => <SupportSvg css={iconSvg} />,
    [],
  );

  return (
    <div css={container} {...remainingProps}>
      {webShareApiIsSupported ? (
        <SocialMediaShareLinkList
          itemIconColor={colors.secondary500}
          itemSize="1.5rem"
          serviceItemCss={socialMediaShareLinkListServiceItem}
          title={tool.name}
          url={absoluteUrl}
        />
      ) : (
        <>
          <Media greaterThanOrEqual="singleColumn">
            <SocialMediaShareLinkList
              itemIconColor={colors.secondary500}
              itemSize="1.5rem"
              title={tool.name}
              url={absoluteUrl}
              showSupportIcon
            />
          </Media>

          <Media lessThan="singleColumn">
            <DrawerDialogAndDisclosure
              heading={strings.AppShareAndSupportLinks.shareDialogA11yHeading}
              headingIsVisible={false}
              headingLevel={2}
              animatedDialogStore={shareAnimatedDialogStore}
              disclosureContentElement={shareDialogDisclosureContent}
            >
              <SocialMediaShareLinkList
                itemIconColor={colors.secondary500}
                itemSize="2.5rem"
                title="{children}"
                url="{children}"
                css={socialShareContainer}
                onItemClick={onMobileSocialMediaShareLinkListItemClick}
              />
            </DrawerDialogAndDisclosure>

            <DrawerDialogAndDisclosure
              heading={strings.AppShareAndSupportLinks.supportDialogHeading}
              headingLevel={2}
              animatedDialogStore={supportAnimatedDialogStore}
              disclosureContentElement={supportDialogDisclosureContent}
            >
              <DrawerDialogLinksContent
                routeInfos={supportDialogRouteInfos}
                animatedDialogState={supportAnimatedDialogStore}
              />
            </DrawerDialogAndDisclosure>
          </Media>
        </>
      )}
    </div>
  );
});

AppShareAndSupportLinks.displayName = "AppShareAndSupportLinks";

export default AppShareAndSupportLinks;
