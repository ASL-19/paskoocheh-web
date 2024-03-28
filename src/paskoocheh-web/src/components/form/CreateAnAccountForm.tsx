import { focusElement } from "@asl-19/js-dom-utils";
import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import Link from "next/link";
import {
  FormEventHandler,
  memo,
  useCallback,
  useEffect,
  useId,
  useRef,
} from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import { GqlDoSignUp } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import {
  formButton,
  formContainer,
  formDescription,
  formDescriptionLink,
  formInput,
  formLabel,
  inputGroup,
} from "src/styles/formStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

// ==============================
// ===== Next.js component ======
// ==============================
const CreateAnAccountForm: StylableFC<{ referralSlug: string | null }> = memo(
  ({ referralSlug, ...remainingProps }) => {
    const { localeCode } = useAppLocaleInfo();
    const { CreateAnAccountPage: strings, shared: sharedStrings } =
      useAppStrings();
    const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

    // handle errors
    const {
      confirmationMessageElementRef,
      errorMessagesListRef,
      formState,
      setFormState,
    } = useFormStateAndFocusManagement();

    const usernameInputRef = useRef<HTMLInputElement>(null);
    const emailInputRef = useRef<HTMLInputElement>(null);
    const password1InputRef = useRef<HTMLInputElement>(null);
    const password2InputRef = useRef<HTMLInputElement>(null);

    const onFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
      async (event) => {
        event.preventDefault();

        setFormState({ type: "isSubmitting" });

        let registerResponse: GqlDoSignUp;

        try {
          const graphQlSdk = await getGraphQlSdk({ method: "POST" });
          registerResponse = await graphQlSdk.doSignUp({
            email: emailInputRef.current?.value ?? "",
            password1: password1InputRef.current?.value ?? "",
            password2: password2InputRef.current?.value ?? "",
            referralSlug,
            username: usernameInputRef.current?.value ?? "",
          });
        } catch {
          setFormState({
            errorMessages: [sharedStrings.form.errorMessages.network],
            type: "hasErrorMessages",
          });
          return;
        }

        if (registerResponse.register.errors) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError: registerResponse.register.errors,
          });

          setFormState({ errorMessages, type: "hasErrorMessages" });
          return;
        }

        setFormState({ type: "isSubmitted" });
      },
      [referralSlug, setFormState, sharedStrings.form.errorMessages.network],
    );

    useEffect(() => {
      if (formState.type === "hasErrorMessages") {
        focusElement(errorMessagesListRef.current);
      } else if (formState.type === "isSubmitted") {
        focusElement(confirmationMessageElementRef.current);
      }
    }, [confirmationMessageElementRef, errorMessagesListRef, formState]);

    const onFormInput = useCallback(() => {
      if (formState.type === "hasErrorMessages") {
        setFormState({ type: "isNotSubmitted" });
      }
    }, [formState.type, setFormState]);

    const id = useId();

    const usernameInputId = `${id}-username`;
    const emailInputId = `${id}-email`;
    const password1InputId = `${id}-password1`;
    const password2InputId = `${id}-password2`;

    return (
      <form
        css={formContainer}
        onSubmit={onFormSubmit}
        onInput={onFormInput}
        {...remainingProps}
      >
        <div css={inputGroup}>
          <label css={formLabel} htmlFor={usernameInputId}>
            {strings.usernameLabel}
          </label>
          <input
            css={formInput}
            id={usernameInputId}
            placeholder=""
            ref={usernameInputRef}
            required
            type="text"
          />
        </div>

        <div css={inputGroup}>
          <label css={formLabel} htmlFor={emailInputId}>
            {strings.emailLabel}
          </label>
          <input
            css={formInput}
            id={emailInputId}
            placeholder=""
            ref={emailInputRef}
            required
            type="email"
          />
        </div>

        <div css={inputGroup}>
          <label css={formLabel} htmlFor={password1InputId}>
            {strings.passwordLabel}
          </label>
          <input
            css={formInput}
            id={password1InputId}
            placeholder=""
            ref={password1InputRef}
            required
            type="password"
          />
        </div>

        <div css={inputGroup}>
          <label css={formLabel} htmlFor={password2InputId}>
            {strings.reenterPasswordLabel}
          </label>
          <input
            css={formInput}
            id={password2InputId}
            placeholder=""
            ref={password2InputRef}
            required
            type="password"
          />
        </div>

        <FormSubmitButton
          text={strings.submitButton}
          formState={formState}
          css={formButton}
        />

        {formState.type === "isSubmitted" && (
          <p ref={confirmationMessageElementRef}>{strings.confirmation}</p>
        )}

        <div css={formDescription}>
          {strings.signInText}
          <Link
            href={routeUrls.signIn({
              localeCode,
              platform: queryOrDefaultPlatformSlug,
            })}
            css={formDescriptionLink}
          >
            {strings.signInLink}
          </Link>
        </div>

        <FormErrorMessages
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </form>
    );
  },
);

CreateAnAccountForm.displayName = "CreateAnAccountForm";

export default CreateAnAccountForm;
