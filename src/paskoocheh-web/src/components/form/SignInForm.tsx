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
import { GqlDoTokenAuth } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import {
  useAppDispatch,
  useAppLocaleInfo,
  useAppStrings,
} from "src/stores/appStore";
import {
  formButton,
  formContainer,
  formDescription,
  formDescriptionLink,
  inputGroup,
} from "src/styles/formStyles";
import { formInput, formLabel } from "src/styles/formStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import setRefreshToken from "src/utils/api/setRefreshToken";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

// ==============================
// ===== Next.js component ======
// ==============================
const SignInForm: StylableFC = memo((props) => {
  const { localeCode } = useAppLocaleInfo();
  const { SignInPage: strings, shared: sharedStrings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();
  const appDispatch = useAppDispatch();

  // handle errors
  const {
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    setFormState,
  } = useFormStateAndFocusManagement();

  const usernameInputRef = useRef<HTMLInputElement>(null);
  const passwordInputRef = useRef<HTMLInputElement>(null);

  const onFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
    async (event) => {
      event.preventDefault();

      setFormState({ type: "isSubmitting" });

      const username = usernameInputRef.current?.value ?? "";
      const password = passwordInputRef.current?.value ?? "";

      let tokenAuthResponse: GqlDoTokenAuth;

      const graphQlSdk = await getGraphQlSdk({ method: "POST" });

      try {
        tokenAuthResponse = await graphQlSdk.doTokenAuth({
          password,
          username,
        });
      } catch {
        setFormState({
          errorMessages: [sharedStrings.form.errorMessages.network],
          type: "hasErrorMessages",
        });
        return;
      }

      if (tokenAuthResponse.tokenAuth.errors) {
        const errorMessages = getErrorMessagesFromExpectedError({
          expectedError: tokenAuthResponse.tokenAuth.errors,
        });

        setFormState({ errorMessages, type: "hasErrorMessages" });
        return;
      }

      const refreshToken = tokenAuthResponse.tokenAuth?.refreshToken?.token;
      const responseUsername = tokenAuthResponse.tokenAuth?.user?.username;

      if (refreshToken && responseUsername) {
        setRefreshToken(refreshToken);
        setFormState({ type: "isSubmitted" });

        appDispatch({ type: "usernameChanged", username: responseUsername });
        // SignInPage will redirect user to home now that appStore.user is set
      }
    },
    [appDispatch, setFormState, sharedStrings],
  );

  useEffect(() => {
    if (formState.type === "hasErrorMessages") {
      focusElement(errorMessagesListRef.current);
    } else if (formState.type === "isSubmitted") {
      focusElement(confirmationMessageElementRef.current);
    }
  }, [
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    localeCode,
    queryOrDefaultPlatformSlug,
  ]);

  const id = useId();

  const usernameInputId = `${id}-username`;
  const passwordInputId = `${id}-password`;

  return (
    <form css={formContainer} onSubmit={onFormSubmit} {...props}>
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
        <Link
          href={routeUrls.resetPasswordRequest({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          css={formDescriptionLink}
        >
          {strings.forgotPassword}
        </Link>
      </div>

      <FormErrorMessages
        errorMessagesListRef={errorMessagesListRef}
        formState={formState}
      />

      <FormSubmitButton
        text={strings.submitButton}
        formState={formState}
        css={formButton}
      />

      {formState.type === "isSubmitted" && (
        <p ref={confirmationMessageElementRef}>{strings.confirmation}</p>
      )}

      <div css={formDescription}>
        {strings.signUpText}
        <Link
          href={routeUrls.createAnAccount({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          })}
          css={formDescriptionLink}
        >
          {strings.signUpLink}
        </Link>
      </div>
    </form>
  );
});

SignInForm.displayName = "SignInForm";

export default SignInForm;
