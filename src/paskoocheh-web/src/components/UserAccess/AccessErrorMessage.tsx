import { css } from "@emotion/react";
import { FC, memo } from "react";

import ButtonLink from "src/components/ButtonLink";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";

export type AccessErrorMessageStrings = {
  /**
   * Error message that appears if Certificate Page has failed to load
   */
  headingText: string;
};

const container = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  minHeight: "50rem",
  paddingTop: "3rem",
  rowGap: "1rem",
});

const AccessErrorMessage: FC<{ errorMessage: string }> = memo(
  ({ errorMessage }) => {
    const { localeCode } = useAppLocaleInfo();
    const { AccessErrorMessage: strings, shared: sharedStrings } =
      useAppStrings();
    const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

    return (
      <div css={container}>
        <h2>{strings.headingText}!!!</h2>
        <p>{errorMessage}</p>
        <ButtonLink
          variant="primary"
          text={sharedStrings.button.goToHomePage}
          href={routeUrls.home({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
        />
      </div>
    );
  },
);
AccessErrorMessage.displayName = "AccessErrorMessage";
export default memo(AccessErrorMessage);
