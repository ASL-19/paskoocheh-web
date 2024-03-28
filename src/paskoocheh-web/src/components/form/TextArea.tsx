import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import {
  AriaAttributes,
  ChangeEventHandler,
  Dispatch,
  memo,
  SetStateAction,
  useCallback,
  useId,
} from "react";

import { formInputAndLabelContainer, formLabel } from "src/styles/formStyles";
import { paragraphP1Regular } from "src/styles/typeStyles";
import colors from "src/values/colors";

const textArea = css(
  paragraphP1Regular,
  {
    backgroundColor: colors.shadesWhite,
    border: `1px solid ${colors.neutral500}`,
    borderRadius: "0.25rem",
    color: colors.secondary500,
    minHeight: "12.25rem",
    padding: "0.5rem 1rem",
    resize: "none",
    width: "100%",
  },
  {
    ":focus": {
      borderColor: colors.primary500,
    },
  },
);

const TextArea: StylableFC<
  {
    label: string;
    /**
     * `name` attribute of `textarea` element. May be useful for forms that have
     * POST fallbacks for no-JS users.
     */
    name?: string;
    placeholder: string;
    required?: boolean;
    setValue: Dispatch<SetStateAction<string>>;
    value: string;
  } & AriaAttributes
> = memo(
  ({
    className,
    label,
    name,
    placeholder,
    required,
    setValue,
    value,
    ...ariaAttributes
  }) => {
    const textAreaId = useId();

    const onChange: ChangeEventHandler<HTMLTextAreaElement> = useCallback(
      (event) => {
        setValue(event.target.value);
      },
      [setValue],
    );

    return (
      <div className={className} css={formInputAndLabelContainer}>
        <label css={formLabel} htmlFor={textAreaId}>
          {label}
        </label>
        <textarea
          placeholder={placeholder}
          onChange={onChange}
          id={textAreaId}
          required={required}
          rows={5}
          value={value}
          css={textArea}
          name={name}
          {...ariaAttributes}
        />
      </div>
    );
  },
);

TextArea.displayName = "TextArea";

export default TextArea;
