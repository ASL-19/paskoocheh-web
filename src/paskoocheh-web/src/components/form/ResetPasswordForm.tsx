import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { useRouter } from "next/router";
import { FormEventHandler, memo, useCallback, useId, useRef } from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import { GqlDoPasswordReset } from "src/generated/graphQl";
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

const ResetPasswordForm: StylableFC<{}> = memo(({ className }) => {
  const { ResetPasswordPage: strings, shared: sharedStrings } = useAppStrings();
  const router = useRouter();

  const passwordInputRef = useRef<HTMLInputElement>(null);
  const passwordConfirmInputRef = useRef<HTMLInputElement>(null);

  // handle errors
  const {
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    setFormState,
  } = useFormStateAndFocusManagement();

  const onResetPasswordFormSubmit: FormEventHandler<HTMLFormElement> =
    useCallback(
      async (event) => {
        event.preventDefault();

        setFormState({ type: "isSubmitting" });

        const newPassword1 = passwordInputRef.current?.value ?? "";
        const newPassword2 = passwordConfirmInputRef.current?.value ?? "";
        const token =
          (Array.isArray(router.query.token)
            ? router.query.token[0]
            : router.query.token) ?? "";

        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        let passwordResetResponse: GqlDoPasswordReset;

        try {
          passwordResetResponse = await graphQlSdk.doPasswordReset({
            newPassword1,
            newPassword2,
            token,
          });
        } catch {
          setFormState({
            errorMessages: [sharedStrings.form.errorMessages.network],
            type: "hasErrorMessages",
          });
          return;
        }

        if (passwordResetResponse.passwordReset.errors) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError: passwordResetResponse.passwordReset.errors,
          });

          setFormState({ errorMessages, type: "hasErrorMessages" });
          return;
        }

        setFormState({
          type: "isSubmitted",
        });
      },
      [
        setFormState,
        router.query.token,
        sharedStrings.form.errorMessages.network,
      ],
    );

  const onFormInput: FormEventHandler<HTMLFormElement> = useCallback(() => {
    if (formState.type === "hasErrorMessages") {
      setFormState({ type: "isNotSubmitted" });
    }
  }, [formState.type, setFormState]);

  const id = useId();
  const passwordInputId = `${id}-password`;
  const confirmPasswordInputId = `${id}-confirm-password`;

  return (
    <form
      className={className}
      css={formContainer}
      onInput={onFormInput}
      onSubmit={onResetPasswordFormSubmit}
    >
      <div className={className} css={formInputAndLabelContainer}>
        <label css={formLabel} htmlFor={passwordInputId}>
          {strings.passwordLabel}
        </label>
        <input
          css={formInput}
          id={passwordInputId}
          placeholder=""
          ref={passwordInputRef}
          required
          type="password"
        />

        <label css={formLabel} htmlFor={confirmPasswordInputId}>
          {strings.reenterPasswordLabel}
        </label>
        <input
          css={formInput}
          id={confirmPasswordInputId}
          placeholder=""
          ref={passwordConfirmInputRef}
          required
          type="password"
        />
      </div>

      <div css={inputGroup}>
        <FormErrorMessages
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </div>

      <FormSubmitButton
        text={sharedStrings.button.resetPassword}
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

ResetPasswordForm.displayName = "ResetPasswordForm";

export default ResetPasswordForm;
