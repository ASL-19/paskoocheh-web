import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { FormEventHandler, memo, useCallback, useState } from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import Input from "src/components/form/Input";
import SimpleAppInfo from "src/components/form/SimpleAppInfo";
import TextArea from "src/components/form/TextArea";
import { GqlVersionPreview } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import {
  formButton,
  formConfirmationMessage,
  formContainer,
  inputGroup,
} from "src/styles/formStyles";

const WriteYourMessageForm: StylableFC<{
  versionPreview: GqlVersionPreview | null;
}> = memo(({ versionPreview, ...remainingProps }) => {
  const { shared: sharedStrings } = useAppStrings();

  // handle errors
  const {
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    setFormState,
  } = useFormStateAndFocusManagement();

  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const onContactFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
    async (event) => {
      event.preventDefault();

      setFormState({ type: "isSubmitting" });

      // const emailValue = email ?? "";
      // const messageValue = message ?? "";

      // TODO: Hook this up to the backend, and when we do make sure we include
      // the platform since it will help outreach team (may need to ask backend
      // to add a new argument)

      try {
        setFormState({
          type: "isSubmitted",
        });
      } catch {
        setFormState({
          errorMessages: ["sharedStrings.form.errorMessageGeneric"],
          type: "hasErrorMessages",
        });
      }
    },
    [setFormState],
  );

  const onFormInput: FormEventHandler<HTMLFormElement> = useCallback(() => {
    if (formState.type === "hasErrorMessages") {
      setFormState({ type: "isNotSubmitted" });
    }
  }, [formState.type, setFormState]);

  return (
    <form
      css={formContainer}
      onInput={onFormInput}
      onSubmit={onContactFormSubmit}
      {...remainingProps}
    >
      {versionPreview && <SimpleAppInfo versionPreview={versionPreview} />}
      <Input
        css={inputGroup}
        label={sharedStrings.form.emailLabel}
        type="email"
        setValue={setEmail}
        placeholder={sharedStrings.form.emailPlaceholder}
        required
        value={email}
      />

      <TextArea
        css={inputGroup}
        label={sharedStrings.form.messageLabel}
        setValue={setMessage}
        placeholder={sharedStrings.form.messagePlaceholder}
        required
        value={message}
      />

      <div css={inputGroup}>
        <FormErrorMessages
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </div>

      <FormSubmitButton
        text={sharedStrings.button.submit}
        formState={formState}
        css={formButton}
      />

      {formState.type === "isSubmitted" && (
        <div ref={confirmationMessageElementRef}>
          <p css={formConfirmationMessage}>{"Message Submitted"}</p>
        </div>
      )}
    </form>
  );
});

WriteYourMessageForm.displayName = "WriteYourMessageForm";

export default WriteYourMessageForm;
