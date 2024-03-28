import { invisible } from "@asl-19/emotion-utils";
import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { FormEventHandler, memo, useCallback, useState } from "react";

import DeleteAccountOverlay from "src/components/AccountSettings/DeleteAccountOverlay";
import ButtonDisclosure from "src/components/ButtonDisclosure";
import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import Input from "src/components/form/Input";
import { GqlDoChangePassword, GqlMinimalUser } from "src/generated/graphQl";
import useAnimatedDialogStore from "src/hooks/useAnimatedDialogState";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { formButton, formContainer, inputGroup } from "src/styles/formStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import removeRefreshToken from "src/utils/api/removeRefreshToken";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import colors from "src/values/colors";

// ==============
// === Styles ===
// ==============
const formFieldContainer = css(inputGroup, {
  borderBottom: `2px solid ${colors.secondary100}`,
  display: "flex",
  flexDirection: "column",
  paddingBottom: "2.25rem",
  rowGap: "1.25rem",
});

const button = css({
  marginTop: "1rem",
});

const buttonUpdate = css(formButton, {
  alignSelf: "center",
});

const buttonDelete = css(formButton, button, {
  borderColor: colors.error500,
  color: colors.error500,
});

const AccountSettingsForm: StylableFC<{ user: GqlMinimalUser }> = memo(
  ({ className, user, ...remainingProps }) => {
    const strings = useAppStrings();
    const { localeCode } = useAppLocaleInfo();
    const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

    const [email, setEmail] = useState(user.email);
    const [confirmPassword, setConfirmPassword] = useState("");
    const [oldPassword, setOldPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [username, setUsername] = useState(user.username);
    const router = useRouter();
    // handle errors
    const {
      confirmationMessageElementRef,
      errorMessagesListRef,
      formState,
      setFormState,
    } = useFormStateAndFocusManagement();

    const deleteOverlayDialogStore = useAnimatedDialogStore();
    const deleteOverlayDialogIsMounted =
      deleteOverlayDialogStore.useState("mounted");

    const onUpdateFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
      async (event) => {
        event.preventDefault();

        setFormState({ type: "isSubmitting" });

        const oldPasswordValue = oldPassword ?? "";
        const newPasswordValue = newPassword ?? "";
        const confirmPasswordValue = confirmPassword ?? "";

        let passwordChangeResponse: GqlDoChangePassword | null = null;

        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        try {
          passwordChangeResponse = await graphQlSdk.doChangePassword({
            newPassword1: newPasswordValue,
            newPassword2: confirmPasswordValue,
            oldPassword: oldPasswordValue,
          });
        } catch {
          setFormState({
            errorMessages: [strings.shared.errorMessages.networkError],
            type: "hasErrorMessages",
          });
        }

        if (passwordChangeResponse?.passwordChange.errors) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError: passwordChangeResponse?.passwordChange.errors,
          });

          setFormState({ errorMessages, type: "hasErrorMessages" });
          return;
        }

        removeRefreshToken();
        setFormState({
          type: "isSubmitted",
        });
        router.push(
          routeUrls.accountSettingsSuccess({
            localeCode,
            platform: queryOrDefaultPlatformSlug,
          }),
        );
      },
      [
        confirmPassword,
        localeCode,
        newPassword,
        oldPassword,
        queryOrDefaultPlatformSlug,
        router,
        setFormState,
        strings,
      ],
    );

    const onFormInput: FormEventHandler<HTMLFormElement> = useCallback(() => {
      if (formState.type === "hasErrorMessages") {
        setFormState({ type: "isNotSubmitted" });
      }
    }, [formState.type, setFormState]);

    return (
      <div css={formContainer} {...remainingProps}>
        <form
          className={className}
          css={formFieldContainer}
          onInput={onFormInput}
          onSubmit={onUpdateFormSubmit}
        >
          <Input
            type="text"
            setValue={setUsername}
            label={strings.AccountSettingsPageContent.usernameLabel}
            placeholder=""
            required
            value={username}
            disabled
          />

          <Input
            label={strings.AccountSettingsPageContent.emailLabel}
            type="email"
            setValue={setEmail}
            placeholder=""
            value={email}
            disabled={true}
          />

          <Input
            label={strings.AccountSettingsPageContent.oldPassword}
            type="password"
            setValue={setOldPassword}
            placeholder=""
            required
            value={oldPassword}
          />

          <Input
            label={strings.AccountSettingsPageContent.passwordLabel}
            type="password"
            setValue={setNewPassword}
            placeholder=""
            required
            value={newPassword}
          />

          <Input
            type="password"
            setValue={setConfirmPassword}
            label={strings.AccountSettingsPageContent.reenterPasswordLabel}
            placeholder=""
            required
            value={confirmPassword}
          />

          <div css={inputGroup}>
            <FormErrorMessages
              errorMessagesListRef={errorMessagesListRef}
              formState={formState}
            />
          </div>

          {/* Note: this is never seen and will only be focussed for a split
          second before redirecting to AccountSettingsConfirmationPage. Ideally
          we’d fix this by adjusting useFormStateAndFocusManagement but it’s
          not worth the trouble here. */}
          {formState.type === "isSubmitted" && (
            <p css={invisible} ref={confirmationMessageElementRef}>
              {strings.AccountSettingsPageContent.updatedConfirmationText}
            </p>
          )}

          <FormSubmitButton
            text={strings.AccountSettingsPageContent.buttonUpdate}
            formState={formState}
            css={buttonUpdate}
          />
        </form>

        <ButtonDisclosure
          css={buttonDelete}
          store={deleteOverlayDialogStore}
          text={strings.AccountSettingsPageContent.buttonDelete}
          variant="secondary"
        />
        {deleteOverlayDialogIsMounted && (
          <DeleteAccountOverlay dialogStore={deleteOverlayDialogStore} />
        )}
      </div>
    );
  },
);

AccountSettingsForm.displayName = "AccountSettingsForm";

export default AccountSettingsForm;
