import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { FormEventHandler, memo, useCallback, useId, useRef } from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import { GqlDoSendPasswordResetEmail } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import {
  formButton,
  formConfirmationMessage,
  formContainer,
  formInput,
  formInputAndLabelContainer,
  formLabel,
  inputGroup,
} from "src/styles/formStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

const ResetPasswordRequestForm: StylableFC<{}> = memo(({ className }) => {
  const { ResetPasswordRequestPage: strings, shared: sharedStrings } =
    useAppStrings();

  const emailInputRef = useRef<HTMLInputElement>(null);

  // handle errors
  const {
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    setFormState,
  } = useFormStateAndFocusManagement();

  const onResetPasswordRequestFormSubmit: FormEventHandler<HTMLFormElement> =
    useCallback(
      async (event) => {
        event.preventDefault();

        setFormState({ type: "isSubmitting" });

        const email = emailInputRef.current?.value ?? "";

        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        let sendPasswordResetEmailResponse: GqlDoSendPasswordResetEmail;

        try {
          sendPasswordResetEmailResponse =
            await graphQlSdk.doSendPasswordResetEmail({
              email,
            });
        } catch {
          setFormState({
            errorMessages: [sharedStrings.form.errorMessages.network],
            type: "hasErrorMessages",
          });
          return;
        }

        if (sendPasswordResetEmailResponse.sendPasswordResetEmail.errors) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError:
              sendPasswordResetEmailResponse.sendPasswordResetEmail.errors,
          });

          setFormState({ errorMessages, type: "hasErrorMessages" });
          return;
        }

        setFormState({
          type: "isSubmitted",
        });
      },
      [setFormState, sharedStrings.form.errorMessages.network],
    );

  const onFormInput: FormEventHandler<HTMLFormElement> = useCallback(() => {
    if (formState.type === "hasErrorMessages") {
      setFormState({ type: "isNotSubmitted" });
    }
  }, [formState.type, setFormState]);

  const id = useId();
  const emailInputId = `${id}-email`;

  return (
    <form
      className={className}
      css={formContainer}
      onInput={onFormInput}
      onSubmit={onResetPasswordRequestFormSubmit}
    >
      <div className={className} css={formInputAndLabelContainer}>
        <label css={formLabel} htmlFor={emailInputId}>
          {sharedStrings.form.emailLabel}
        </label>
        <input
          css={formInput}
          id={emailInputId}
          placeholder={sharedStrings.form.emailPlaceholder}
          ref={emailInputRef}
          required
          type="email"
        />
      </div>

      <div css={inputGroup}>
        <FormErrorMessages
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </div>

      <FormSubmitButton
        text={sharedStrings.button.send}
        formState={formState}
        css={formButton}
      />

      {formState.type === "isSubmitted" && (
        <div className={className} ref={confirmationMessageElementRef}>
          <p css={formConfirmationMessage}>{strings.confirmation}</p>
        </div>
      )}
    </form>
  );
});

ResetPasswordRequestForm.displayName = "ResetPasswordRequestForm";

export default ResetPasswordRequestForm;
