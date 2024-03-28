import { match } from "ts-pattern";

import { buttonPrimary, buttonSecondary } from "src/styles/buttonStyles";
import { ButtonSize, ButtonVariant } from "src/types/buttonTypes";

const getButtonCss = ({
  disabled,
  size,
  variant,
}: {
  disabled?: boolean;
  size: ButtonSize;
  variant: ButtonVariant;
}) =>
  match(variant)
    .with("primary", () => buttonPrimary({ disabled, size }))
    .with("secondary", () => buttonSecondary({ disabled, size }))
    .exhaustive();

export default getButtonCss;
