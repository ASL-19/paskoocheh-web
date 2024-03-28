import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import FacebookSvg from "src/components/icons/social/FacebookSvg";
import InstagramSvg from "src/components/icons/social/InstagramSvg";
import MailSvg from "src/components/icons/social/MailSvg";
import TelegramSvg from "src/components/icons/social/TelegramSvg";
import TwitterSvg from "src/components/icons/social/TwitterSvg";
import SocialMediaLinkListItem, {
  SocialMediaListItemStyleProps,
} from "src/components/SocialMediaLinkListItem";
import { useAppStrings } from "src/stores/appStore";

const list = ({ itemSize }: { itemSize: string }) =>
  css({
    alignItems: "center",
    display: "flex",
    flex: "0 0 auto",
    flexDirection: "row",
    gap: `calc(${itemSize} / 2)`,
    maxWidth: "100%",
  });

const SocialMediaLinkList: StylableFC<
  SocialMediaListItemStyleProps & {
    emailUsername?: string;
    facebookUsername?: string;
    instagramUsername?: string;
    telegramUsername?: string;
    twitterUsername?: string;
  }
> = memo(
  ({
    className,
    emailUsername,
    facebookUsername,
    instagramUsername,
    itemHoverIconColor,
    itemIconColor,
    itemSize,
    telegramUsername,
    twitterUsername,
  }) => {
    const strings = useAppStrings();

    const itemStyleProps: SocialMediaListItemStyleProps = {
      itemHoverIconColor,
      itemIconColor,
      itemSize,
    };

    return (
      <ul className={className} css={list({ itemSize })}>
        {twitterUsername && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.twitter}
            IconComponent={TwitterSvg}
            href={`https://twitter.com/${twitterUsername}`}
          />
        )}

        {telegramUsername && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.telegram}
            IconComponent={TelegramSvg}
            href={`https://t.me/${telegramUsername}`}
          />
        )}

        {instagramUsername && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.instagram}
            IconComponent={InstagramSvg}
            href={`https://www.instagram.com/${instagramUsername}`}
          />
        )}
        {facebookUsername && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.facebook}
            IconComponent={FacebookSvg}
            href={`https://www.facebook.com/${facebookUsername}`}
          />
        )}

        {emailUsername && (
          <SocialMediaLinkListItem
            {...itemStyleProps}
            iconAriaLabel={strings.shared.socialMediaPlatformNames.email}
            IconComponent={MailSvg}
            href={`mailto:${emailUsername}`}
          />
        )}
      </ul>
    );
  },
);

SocialMediaLinkList.displayName = "SocialMediaLinkList";

export default SocialMediaLinkList;
