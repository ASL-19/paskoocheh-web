import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ThumbsUpSvg from "src/components/icons/general/ThumbsUpSvg";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type CreateAnAccountReferralMessageStrings = {
  /**
   * Text for user that create account from referral
   */
  message: string;
};

const container = css({
  background: colors.secondary50,
  display: "flex",
  justifyContent: "center",
  margin: "0 -150rem",
});
const icon = css({
  height: "1.5rem",
});

const centeredContainer = css({
  display: "flex",
  gap: "0.5rem",
  padding: "1rem",
});

const CreateAnAccountReferralMessage: StylableFC = memo(
  ({ ...remainingProps }) => {
    const { CreateAnAccountReferralMessage: strings } = useAppStrings();

    return (
      <div css={container} {...remainingProps}>
        <div css={centeredContainer}>
          <ThumbsUpSvg css={icon} />
          <p>{strings.message}</p>
        </div>
      </div>
    );
  },
);

CreateAnAccountReferralMessage.displayName = "CreateAnAccountReferralMessage";

export default CreateAnAccountReferralMessage;
