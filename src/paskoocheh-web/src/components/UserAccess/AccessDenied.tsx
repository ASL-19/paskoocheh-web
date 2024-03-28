import { css } from "@emotion/react";
import Image from "next/image";
import { useRouter } from "next/router";
import { FC, memo } from "react";

import ButtonLink from "src/components/ButtonLink";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import accessDenied from "src/static/images/accessDenied.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { paragraphP1SemiBold } from "src/styles/typeStyles";
export type AccessDeniedStrings = {
  /**
   * Button text notifies that it navigates a user to a "Sign in" page
   */
  buttonText: string;
  /**
   * "Sign in to enjoy more"
   *
   * Text that appears if user is not singed in
   */
  text: string;
};

const container = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  minHeight: "50rem",
  paddingTop: "5rem",
  rowGap: "1.5rem",
});

const illustrationWidth = "10rem";

const illustration = css({
  height: "auto",
  width: illustrationWidth,
});

const AccessDenied: FC = memo(() => {
  const router = useRouter();

  const { localeCode } = useAppLocaleInfo();
  const { AccessDenied: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <div css={container}>
      <Image
        src={accessDenied}
        css={illustration}
        alt=""
        sizes={illustrationWidth}
      />
      <p css={paragraphP1SemiBold}>{strings.text}</p>
      <ButtonLink
        text={strings.buttonText}
        variant="primary"
        href={routeUrls.signIn({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          returnPath: encodeURIComponent(router.asPath),
        })}
      />
    </div>
  );
});

AccessDenied.displayName = "AccessDenied";

export default AccessDenied;
