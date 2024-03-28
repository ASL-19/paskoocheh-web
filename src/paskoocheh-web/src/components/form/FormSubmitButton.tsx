import { FormState, StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ButtonButton from "src/components/ButtonButton";
import LoadingIndicatorSvg from "src/components/icons/animation/LoadingIndicatorSvg";
import { buttonHeights } from "src/values/layoutValues";

const loadingIndicatorSvg = css({
  display: "block",
  height: buttonHeights.medium,
  transform: "scale(2)",
  width: buttonHeights.medium,
});

const FormSubmitButton: StylableFC<{
  disabled?: boolean;
  formState: FormState;
  text: string;
}> = memo(({ disabled, formState, text, ...otherProps }) =>
  formState.type === "isSubmitting" ? (
    <LoadingIndicatorSvg css={loadingIndicatorSvg} {...otherProps} />
  ) : (
    <ButtonButton
      disabled={disabled}
      text={text}
      variant="primary"
      {...otherProps}
    />
  ),
);

FormSubmitButton.displayName = "FormSubmitButton";

export default FormSubmitButton;
