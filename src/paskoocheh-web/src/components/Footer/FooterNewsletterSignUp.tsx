import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { FormEvent, memo, useCallback, useRef } from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import PageSegment from "src/components/Page/PageSegment";
import { useAppStrings } from "src/stores/appStore";
import { formInput } from "src/styles/formStyles";
import { paragraphP1Regular } from "src/styles/typeStyles";
import colors from "src/values/colors";

export type FooterNewsletterSignUpStrings = {
  /**
   * Text description to subscribe for newsletters
   */
  description: string;
  /**
   * Placeholder text that describes the expected value of a input field
   */
  email: string;
  /**
   * Button text: "Submit" button
   */
  submitButton: string;
};

const container = css({
  padding: "1rem 0",
});

const description = css(paragraphP1Regular, {
  color: colors.shadesWhite,
});

const formFields = css({
  display: "flex",
  flexFlow: "row wrap",
  gap: "1rem",
  margin: "1.25rem auto 0",
});

const emailInput = css(formInput({ disabled: false }), {
  flex: "1",
  maxWidth: "13rem",
});

const formErrorMessages = css({
  textAlign: "center",
});

const emailInputId = "NewsletterSignUpForm-email";

const FooterNewsletterSignUp: StylableFC<{}> = memo(() => {
  const strings = useAppStrings();

  const emailInputRef = useRef<HTMLInputElement>(null);
  const { errorMessagesListRef, formState, setFormState } =
    useFormStateAndFocusManagement();

  // handle submit
  const onNewsletterFormSubmit = useCallback(
    async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();

      setFormState({
        errorMessages: ["Error message"],
        type: "hasErrorMessages",
      });
    },
    [setFormState],
  );

  const onFormInput = useCallback(() => {
    if (formState.type === "hasErrorMessages") {
      setFormState({ type: "isNotSubmitted" });
    }
  }, [formState.type, setFormState]);

  return (
    <PageSegment centeredContainerCss={container}>
      <p css={description}>{strings.FooterNewsletterSignUp.description}</p>

      <form onInput={onFormInput} onSubmit={onNewsletterFormSubmit}>
        <div css={formFields}>
          <input
            css={emailInput}
            type="email"
            placeholder={strings.FooterNewsletterSignUp.email}
            id={emailInputId}
            ref={emailInputRef}
            required
          />
          <FormSubmitButton
            text={strings.FooterNewsletterSignUp.submitButton}
            formState={formState}
          />
        </div>

        <FormErrorMessages
          css={formErrorMessages}
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </form>
    </PageSegment>
  );
});

FooterNewsletterSignUp.displayName = "FooterNewsletterSignUp";

export default FooterNewsletterSignUp;
