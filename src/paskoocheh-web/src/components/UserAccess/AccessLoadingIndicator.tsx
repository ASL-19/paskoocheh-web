import { css } from "@emotion/react";
import { FC, memo, useEffect, useState } from "react";

import LoadingIndicatorSvg from "src/components/icons/animation/LoadingIndicatorSvg";

const container = css({
  alignItems: "center",
  display: "flex",
  height: "100%",
  justifyContent: "center",
  maxWidth: "100%",
  minHeight: "50rem",
  padding: "0 1rem",
});

const loadingIndicatorSvg = css({
  maxWidth: "10rem",
  width: "100%",
});

const AccessLoadingIndicator: FC = memo(() => {
  const [shouldDisplayLoadingIndicator, setShouldDisplayLoadingIndicator] =
    useState(false);

  useEffect(() => {
    const timeoutId = setTimeout(
      () => setShouldDisplayLoadingIndicator(true),
      300,
    );

    return () => clearTimeout(timeoutId);
  }, []);

  return shouldDisplayLoadingIndicator ? (
    <div css={container}>
      <LoadingIndicatorSvg css={loadingIndicatorSvg} />
    </div>
  ) : (
    <div css={container} />
  );
});
AccessLoadingIndicator.displayName = "AccessLoadingIndicator";
export default AccessLoadingIndicator;
