import { StylableFC } from "@asl-19/react-dom-utils";
import {
  AriaAttributes,
  ChangeEventHandler,
  Dispatch,
  memo,
  SetStateAction,
  useCallback,
  useId,
} from "react";

import {
  formInput,
  formInputAndLabelContainer,
  formLabel,
} from "src/styles/formStyles";

const Input: StylableFC<
  {
    disabled?: boolean;
    label: string;
    /**
     * `name` attribute of `input` element. May be useful for forms that have
     * POST fallbacks for no-JS users.
     */
    name?: string;
    placeholder: string;
    required?: boolean;
    setValue: Dispatch<SetStateAction<string>>;
    type?: string;
    value: string;
  } & AriaAttributes
> = memo(
  ({
    className,
    disabled = false,
    label,
    name,
    placeholder,
    required,
    setValue,
    type = "text",
    value,
    ...ariaAttributes
  }) => {
    const inputId = useId();

    const onChange: ChangeEventHandler<HTMLInputElement> = useCallback(
      (event) => {
        setValue(event.target.value);
      },
      [setValue],
    );

    return (
      <div className={className} css={formInputAndLabelContainer}>
        <label css={formLabel} htmlFor={inputId}>
          {label}
        </label>
        <input
          className={className}
          css={formInput({ disabled })}
          type={type}
          id={inputId}
          disabled={disabled}
          required={required}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          name={name}
          {...ariaAttributes}
        />
      </div>
    );
  },
);

Input.displayName = "Input";

export default Input;
