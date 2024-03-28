import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type NoResultsIllustrationAndMessageStrings = {
  message: string;
};

const container = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
});

const message = css({
  color: colors.black,
  fontSize: "1.5rem",
  fontWeight: "700",
  marginBottom: "3rem",
});

const NoResultsIllustrationAndMessage: StylableFC = memo(({ className }) => {
  const { NoResultsIllustrationAndMessage: strings } = useAppStrings();

  return (
    <div className={className} css={container}>
      <p css={message}>{strings.message}</p>
    </div>
  );
});

NoResultsIllustrationAndMessage.displayName = "NoResultsIllustrationAndMessage";

export default NoResultsIllustrationAndMessage;
