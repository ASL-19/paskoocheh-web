import { announce } from "@asl-19/js-dom-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, MouseEventHandler, useCallback, useState } from "react";
import { match } from "ts-pattern";

import CopySvg from "src/components/icons/general/CopySvg";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  dashboardItemContainer,
  dashboardItemTitle,
} from "src/styles/dashboardStyles";
import { formInput } from "src/styles/formStyles";
import colors from "src/values/colors";

export type RewardsReferralLinkStrings = {
  copyButtonA11yLabel: string;
  copyFailTooltip: string;
  copySuccessTooltip: string;
};

const linkContainer = css(formInput({ disabled: false }), {
  display: "flex",
  justifyContent: "space-between",
});
const link = css({ width: "100%" });
const icon = css({ height: "1rem" });
const iconContainer = css({
  alignItems: "center",
  backgroundColor: colors.shadesWhite,
  display: "flex",
  justifyContent: "center",
  position: "relative",
  width: "2rem",
});

const tooltip = css({
  backgroundColor: colors.shadesWhite,
  border: `1px solid ${colors.secondary100}`,
  borderRadius: "0.5rem",
  padding: "0 1rem",
  position: "absolute",
  textIndent: 0,
  top: "-3rem",
  whiteSpace: "nowrap",
});

const RewardsReferralLink: StylableFC<{ referralSlug: string }> = memo(
  ({ className, referralSlug }) => {
    const { localeCode } = useAppLocaleInfo();
    const strings = useAppStrings();
    const [didCopySuccessfully, setDidCopySuccessfully] = useState<
      boolean | undefined
    >(undefined);

    const referralFullyQualifiedUrl = `${process.env.NEXT_PUBLIC_WEB_URL}${routeUrls.createAnAccount(
      {
        localeCode,
        referral: referralSlug,
      },
    )}`;

    const onClick = useCallback<MouseEventHandler<HTMLButtonElement>>(
      async (event) => {
        event.preventDefault();

        try {
          await navigator.clipboard.writeText(referralFullyQualifiedUrl);
          setDidCopySuccessfully(true);
          announce({
            priority: "assertive",
            text: strings.RewardsReferralLink.copySuccessTooltip,
          });
        } catch {
          setDidCopySuccessfully(false);
          announce({
            priority: "assertive",
            text: strings.RewardsReferralLink.copyFailTooltip,
          });
        }

        setTimeout(() => setDidCopySuccessfully(undefined), 1000);
      },
      [
        referralFullyQualifiedUrl,
        strings.RewardsReferralLink.copyFailTooltip,
        strings.RewardsReferralLink.copySuccessTooltip,
      ],
    );

    return (
      <form className={className} css={dashboardItemContainer}>
        <label css={dashboardItemTitle} htmlFor="referralLinkInput">
          {strings.RewardsPageContent.shareYourReferral}
        </label>
        <div css={linkContainer}>
          <input
            css={link}
            value={referralFullyQualifiedUrl}
            id="referralLinkInput"
            readOnly
          />
          <button
            aria-label={strings.RewardsReferralLink.copyButtonA11yLabel}
            css={iconContainer}
            type="submit"
            onClick={onClick}
          >
            {typeof didCopySuccessfully === "boolean" && (
              <div css={tooltip}>
                <span>
                  {match(didCopySuccessfully)
                    .with(
                      true,
                      () => strings.RewardsReferralLink.copySuccessTooltip,
                    )
                    .with(
                      false,
                      () => strings.RewardsReferralLink.copyFailTooltip,
                    )
                    .exhaustive()}
                </span>
              </div>
            )}

            <CopySvg css={icon} />
          </button>
        </div>
      </form>
    );
  },
);

RewardsReferralLink.displayName = "RewardsReferralLink";

export default RewardsReferralLink;
