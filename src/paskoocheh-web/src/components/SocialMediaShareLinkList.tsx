import { StylableFC } from "@asl-19/react-dom-utils";
import { css, SerializedStyles } from "@emotion/react";
import {
  memo,
  MouseEvent,
  MouseEventHandler,
  useCallback,
  useEffect,
  useState,
} from "react";

import ShareSvg from "src/components/icons/general/ShareSvg";
import SupportSvg from "src/components/icons/general/SupportSvg";
import FacebookSvg from "src/components/icons/social/FacebookSvg";
import TelegramSvg from "src/components/icons/social/TelegramSvg";
import TwitterSvg from "src/components/icons/social/TwitterSvg";
import SocialMediaLinkListItem, {
  SocialMediaListItemStyleProps,
} from "src/components/SocialMediaLinkListItem";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";

const list = ({ itemSize }: { itemSize: string }) =>
  css({
    alignItems: "center",
    display: "flex",
    flex: "0 0 auto",
    flexDirection: "row",
    gap: itemSize,
    maxWidth: "100%",
  });

const SocialMediaShareLinkList: StylableFC<
  SocialMediaListItemStyleProps & {
    onItemClick?: MouseEventHandler;
    /**
     * CSS applied to service-specific items (not the native share button).
     */
    serviceItemCss?: SerializedStyles;
    showSupportIcon?: boolean;
    title: string;
    url: string;
  }
> = memo(
  ({
    className,
    itemHoverIconColor,
    itemIconColor,
    itemSize,
    onItemClick,
    serviceItemCss,
    showSupportIcon = false,
    title,
    url,
  }) => {
    const { localeCode } = useAppLocaleInfo();
    const platform = useQueryOrDefaultPlatformSlug();

    const strings = useAppStrings();

    const itemStyleProps: SocialMediaListItemStyleProps = {
      itemHoverIconColor,
      itemIconColor,
      itemSize,
    };

    const encodedTweetText = encodeURIComponent(
      title ? `${title}\n\n${url}` : url,
    );
    const encodedUrl = encodeURIComponent(url);

    const onShareLinkClick = useCallback(
      async (event: MouseEvent<HTMLAnchorElement>) => {
        event.preventDefault();

        try {
          await navigator.share({
            title,
            url,
          });

          if (onItemClick) {
            onItemClick(event);
          }
        } catch {
          console.warn(
            "SocialMediaShareLinkList: Error while calling navigator.share()",
          );
        }
      },
      [title, url, onItemClick],
    );

    const [webShareApiIsSupported, setWebShareApiIsSupported] = useState(true);

    useEffect(() => {
      if (!("share" in navigator)) {
        setWebShareApiIsSupported(false);
      }
    }, []);

    return (
      <ul
        className={className}
        css={list({
          itemSize,
        })}
      >
        <SocialMediaLinkListItem
          {...itemStyleProps}
          IconComponent={TwitterSvg}
          css={serviceItemCss}
          href={`https://twitter.com/intent/tweet?text=${encodedTweetText}`}
          iconAriaLabel={strings.shared.socialMediaPlatformNames.twitter}
          onClick={onItemClick}
        />

        <SocialMediaLinkListItem
          {...itemStyleProps}
          IconComponent={TelegramSvg}
          css={serviceItemCss}
          href={`https://telegram.me/share/url?url=${encodedUrl}`}
          iconAriaLabel={strings.shared.socialMediaPlatformNames.telegram}
          onClick={onItemClick}
        />

        <SocialMediaLinkListItem
          {...itemStyleProps}
          css={serviceItemCss}
          href={`https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`}
          IconComponent={FacebookSvg}
          iconAriaLabel={strings.shared.socialMediaPlatformNames.facebook}
          onClick={onItemClick}
        />

        {webShareApiIsSupported && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.facebook}
            IconComponent={ShareSvg}
            onClick={onShareLinkClick}
          />
        )}

        {showSupportIcon && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            css={serviceItemCss}
            href={routeUrls.contact({ localeCode, platform })}
            IconComponent={SupportSvg}
            iconAriaLabel=""
          />
        )}
      </ul>
    );
  },
);

SocialMediaShareLinkList.displayName = "SocialMediaShareLinkList";

export default SocialMediaShareLinkList;
