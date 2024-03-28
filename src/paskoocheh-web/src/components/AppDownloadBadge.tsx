import { css } from "@emotion/react";
import { ComponentType, FC, memo } from "react";

import { appInstallBadge } from "src/styles/appStyles";

const link = css({
  display: "flex",
});

const AppDownloadBadge: FC<{
  BadgeSvg: ComponentType<{
    className?: string | undefined;
  }>;
  className?: string;
  href?: string;
  label?: string;
}> = memo(({ BadgeSvg, href, label, ...remainingProps }) =>
  href ? (
    <a
      css={link}
      href={href}
      rel="noreferrer"
      target="_blank"
      aria-label={label}
      {...remainingProps}
    >
      <BadgeSvg css={appInstallBadge} />
    </a>
  ) : (
    <BadgeSvg css={appInstallBadge} {...remainingProps} />
  ),
);

AppDownloadBadge.displayName = "AppDownloadBadge";

export default AppDownloadBadge;
