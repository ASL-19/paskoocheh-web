import { useFormStateAndFocusManagement } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import {
  FC,
  FormEventHandler,
  memo,
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
} from "react";

import AnimatedDialog from "src/components/AnimatedDialog";
import ButtonButton from "src/components/ButtonButton";
import ButtonLink from "src/components/ButtonLink";
import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import Input from "src/components/form/Input";
import { AnimatedDialogStore } from "src/hooks/useAnimatedDialogState";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { inputGroup } from "src/styles/formStyles";
import { paragraphP1Regular, paragraphP2SemiBold } from "src/styles/typeStyles";
import getErrorMessagesFromExpectedError from "src/utils/api/getErrorMessagesFromResponseErrorsByFieldKey";
import removeRefreshToken from "src/utils/api/removeRefreshToken";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import colors from "src/values/colors";

export type DeleteAccountOverlayStrings = {
  cancelButton: string;
  confirmationText: string;
  deleteButton: string;
  deleteConfirmationText: string;
  description: string;
  enterPassword: string;
  title: string;
};

const formFieldContainer = css(inputGroup, {
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const dialog = css(
  {
    backgroundColor: colors.shadesWhite,
    borderRadius: "0.5rem",
    maxWidth: "calc(100vw - 2 * 1rem)",
    overflow: "hidden auto",
    padding: "2rem",
    width: "27rem",
  },
  // Vertically and horizontally center without flex container, via:
  // https://github.com/ariakit/ariakit/releases/tag/%40ariakit%2Freact%400.2.0
  {
    height: "fit-content",
    inset: "1rem",
    margin: "auto",
    maxHeight: "calc(100vh - 2 * 1rem)",
    position: "fixed",
  },
);

const buttonsContainer = css({
  columnGap: "0.5rem",
  display: "flex",
  // Allow buttons to wrap if viewport width is very constrained
  flexWrap: "wrap",
  justifyContent: "flex-end",
});

const cancelButton = css({
  border: "none",
  color: colors.secondary400,
});

const formSubmittedContainer = css(formFieldContainer, {
  alignItems: "center",
});

const DeleteAccountOverlay: FC<{
  dialogStore: AnimatedDialogStore;
}> = memo(({ dialogStore }) => {
  const router = useRouter();

  const strings = useAppStrings();
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const dialogRef = useRef<HTMLDivElement>(null);

  const headingId = useId();
  const [password, setPassword] = useState("");

  useEffect(() => {
    // This closes automatically when navigating so the links don't need JS to close the modal
    const onRouteChangeStart = () => {
      dialogStore.hide();
    };

    router.events.on("routeChangeStart", onRouteChangeStart);

    return () => {
      router.events.off("routeChangeStart", onRouteChangeStart);
    };
  }, [dialogStore, router.events]);

  const {
    confirmationMessageElementRef,
    errorMessagesListRef,
    formState,
    setFormState,
  } = useFormStateAndFocusManagement();

  const onCancelClick = useCallback(() => {
    dialogStore.hide();
  }, [dialogStore]);

  const onDeleteSubmit: FormEventHandler<HTMLFormElement> = useCallback(
    async (event) => {
      event.preventDefault();

      setFormState({ type: "isSubmitting" });

      const graphQlSdk = await getGraphQlSdk({ method: "POST" });

      try {
        const deleteAccountResponse = await graphQlSdk.doDeleteAccount({
          password,
        });

        if (deleteAccountResponse?.deleteAccount.errors) {
          const errorMessages = getErrorMessagesFromExpectedError({
            expectedError: deleteAccountResponse?.deleteAccount.errors,
          });

          setFormState({ errorMessages, type: "hasErrorMessages" });
          return;
        }

        removeRefreshToken();
        setFormState({
          type: "isSubmitted",
        });
      } catch {
        setFormState({
          errorMessages: [strings.shared.form.errorMessageGeneric],
          type: "hasErrorMessages",
        });
      }
    },
    [password, setFormState, strings.shared.form.errorMessageGeneric],
  );

  return (
    <AnimatedDialog
      aria-labelledby={headingId}
      css={dialog}
      dialogRef={dialogRef}
      store={dialogStore}
      tabIndex={0}
    >
      {formState.type === "isSubmitted" ? (
        <div css={formSubmittedContainer}>
          <h2
            css={paragraphP1Regular}
            id={headingId}
            ref={confirmationMessageElementRef}
          >
            {strings.DeleteAccountOverlay.deleteConfirmationText}
          </h2>

          <ButtonLink
            text={strings.AccountSettingsPageContent.buttonLink}
            href={routeUrls.home({
              localeCode,
              platform: queryOrDefaultPlatformSlug,
            })}
            variant="secondary"
          />
        </div>
      ) : (
        <div>
          <form css={formFieldContainer} onSubmit={onDeleteSubmit}>
            <h2 css={paragraphP2SemiBold}>
              {strings.DeleteAccountOverlay.enterPassword}
            </h2>
            <Input
              label={""}
              type="password"
              setValue={setPassword}
              placeholder=""
              required
              value={password}
            />
            <div css={buttonsContainer}>
              <div css={inputGroup}>
                <FormErrorMessages
                  errorMessagesListRef={errorMessagesListRef}
                  formState={formState}
                />
              </div>

              <ButtonButton
                onClick={onCancelClick}
                text={strings.DeleteAccountOverlay.cancelButton}
                variant="secondary"
                css={cancelButton}
                type="reset"
              />

              <FormSubmitButton
                text={strings.DeleteAccountOverlay.confirmationText}
                formState={formState}
              />
            </div>
          </form>
        </div>
      )}
    </AnimatedDialog>
  );
});

DeleteAccountOverlay.displayName = "DeleteAccountOverlay";

export default DeleteAccountOverlay;
