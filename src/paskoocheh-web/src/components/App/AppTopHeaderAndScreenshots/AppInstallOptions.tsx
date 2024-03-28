import { useSelectStore } from "@ariakit/react/select";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo, useCallback, useMemo, useState } from "react";
import { match, P } from "ts-pattern";

import AppInstallSelect from "src/components/App/AppTopHeaderAndScreenshots/AppInstallSelect";
import AppInstallSelectPopover from "src/components/App/AppTopHeaderAndScreenshots/AppInstallSelectPopover";
import ButtonButton from "src/components/ButtonButton";
import ButtonLink from "src/components/ButtonLink";
import { useAppStrings } from "src/stores/appStore";
import {
  captionRegular,
  paragraphP1SemiBold,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import { InstallationOption } from "src/types/miscTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import colors from "src/values/colors";

export type AppInstallOptionsStrings = {
  /**
   * Text for option Apple App Store
   */
  appleAppStore: string;
  /**
   * Text for option Direct Download
   */
  directDownload: string;
  /**
   * Text for option Download from Chrome web store
   */
  downloadFromChromeWebStore: string;
  /**
   * Text for option Download from email
   */
  downloadFromEmail: string;
  /**
   * Text for option Download from firefox web store
   */
  downloadFromFireFoxWebStore: string;
  /**
   * Text for option Download from microsoft store
   */
  downloadFromMicrosoftStore: string;

  /**
   * Text for option Download from website
   */
  downloadFromWebsite: string;
  /**
   * Text for option Google Play
   */
  googlePlay: string;
};

const container = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
});

const button = css(paragraphP1SemiBold, {
  alignItems: "center",
  borderRadius: "6.25rem",
  height: "3rem",
  width: "17.5rem",
});

const errorMessageLabel = css(captionRegular, {
  color: colors.error500,
});

const AppInstallOptions: StylableFC<{
  version: ValidVersion;
}> = memo(({ version, ...remainingProps }) => {
  const strings = useAppStrings();

  const [errorMessage, setErrorMessage] = useState("");

  const installationOptions = useMemo<
    [InstallationOption, ...Array<InstallationOption>]
  >(() => {
    const externalInstallationOption = match(version.downloadUrl)
      .returnType<InstallationOption | null>()
      .with(
        P.string.regex(/apple\.com/),
        P.string.regex(/appstore\.com/),
        (downloadUrl) => ({
          downloadUrl,
          name: strings.AppInstallOptions.appleAppStore,
          slug: "APPLE_APP_STORE",
        }),
      )
      .with(P.string.regex(/chrome\.google\.com/), (downloadUrl) => ({
        downloadUrl,
        name: strings.AppInstallOptions.downloadFromChromeWebStore,
        slug: "CHROME_WEB_STORE",
      }))
      .with(P.string.minLength(1), (downloadUrl) => ({
        downloadUrl,
        name: strings.AppInstallOptions.downloadFromWebsite,
        slug: "EXTERNAL_WEBSITE",
      }))
      .otherwise(() => null);

    const internalInstallationOptions: [
      InstallationOption,
      ...Array<InstallationOption>,
    ] = version.canGenerateTempS3Url
      ? [
          {
            downloadUrl: "",
            name: strings.AppInstallOptions.directDownload,
            slug: "S3",
          },
          {
            downloadUrl: `mailto:${version.deliveryEmail}`,
            name: strings.AppInstallOptions.downloadFromEmail,
            slug: "EMAIL",
          },
        ]
      : [
          {
            downloadUrl: `mailto:${version.deliveryEmail}`,
            name: strings.AppInstallOptions.downloadFromEmail,
            slug: "EMAIL",
          },
        ];

    return externalInstallationOption
      ? [externalInstallationOption, ...internalInstallationOptions]
      : internalInstallationOptions;
  }, [strings, version]);

  const selectStore = useSelectStore({
    defaultValue: installationOptions[0].downloadUrl,
  });

  const selectIsMounted = selectStore.useState("mounted");
  const selectValue = selectStore.useState("value");

  const selectedOption =
    installationOptions.find((option) => option.downloadUrl === selectValue) ??
    installationOptions[0];

  const handleDownload = useCallback(async () => {
    if (selectedOption.slug === "EMAIL") {
      return;
    }

    try {
      const graphQlSdk = await getGraphQlSdk({ method: "POST" });

      const saveDownloadResponse = await graphQlSdk.doSaveDownload({
        channelVersion: version.versionNumber,
        downloadVia: selectedOption.slug,
        versionId: version.pk,
      });

      if (!saveDownloadResponse.saveDownload.success) {
        console.error(
          "[AppInstallOptions] Error(s) while save download:",
          saveDownloadResponse.saveDownload.errors,
        );
      }

      if (selectedOption.slug === "S3") {
        const s3Url = await graphQlSdk.getTempS3Url({ versionPk: version.pk });

        if (!s3Url.tempS3Url || !process.env.NEXT_PUBLIC_S3_BUCKET_NAME) {
          setErrorMessage(strings.shared.errorMessages.networkError);
          return;
        }

        window.open(
          s3Url.tempS3Url.startsWith("http")
            ? s3Url.tempS3Url
            : // TODO: Remove if backend now returns absolute URLs?
              `https://s3.amazonaws.com/${process.env.NEXT_PUBLIC_S3_BUCKET_NAME}${s3Url.tempS3Url}`,
        );
      }
    } catch (error) {
      console.error("[AppInstallOptions] Error while saving download:", error);
    }

    window.open(selectedOption.downloadUrl);
  }, [
    selectedOption.downloadUrl,
    selectedOption.slug,
    strings.shared.errorMessages.networkError,
    version.pk,
    version.versionNumber,
  ]);

  return (
    <div css={container} {...remainingProps}>
      <h2 css={paragraphP2SemiBold}>
        {strings.AppOverviewSection.availableOptions}
      </h2>

      <AppInstallSelect selectStore={selectStore} label={selectedOption.name} />

      {selectIsMounted && (
        <AppInstallSelectPopover
          installationOptions={installationOptions}
          selectStore={selectStore}
        />
      )}

      {match(selectedOption)
        .with({ slug: "EMAIL" }, (selectedOption) => (
          <ButtonLink
            css={button}
            href={selectedOption.downloadUrl}
            text={strings.AppOverviewSection.buttonText}
            variant={"primary"}
          />
        ))
        .otherwise(() => (
          <>
            <ButtonButton
              css={button}
              onClick={handleDownload}
              text={strings.AppOverviewSection.buttonText}
              variant={"primary"}
            />

            <p css={errorMessageLabel}>{errorMessage}</p>
          </>
        ))}
    </div>
  );
});

AppInstallOptions.displayName = "AppInstallOptions";

export default AppInstallOptions;
