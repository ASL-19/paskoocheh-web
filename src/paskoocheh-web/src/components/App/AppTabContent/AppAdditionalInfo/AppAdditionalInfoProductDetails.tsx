import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import useDateInfo from "src/hooks/useDateInfo";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { paragraphP2SemiBold } from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import formatNumber from "src/utils/formatNumber";

export type AppAdditionalInfoProductDetailsStrings = {
  /**
   * Text for checksum
   */
  checksum: string;
  /**
   * Text for latest Update date
   */
  latestUpdate: string;
  /**
   * Text for product details title
   */
  productDetails: string;
  /**
   * Text for release date
   */
  releaseDate: string;
  /**
   * Text for size
   */
  size: string;
  /**
   * Text for version
   */
  version: string;
};

const item = css({
  display: "flex",
  gap: "0.25rem",
});

const AppAdditionalInfoProductDetails: StylableFC<{
  version: ValidVersion;
}> = memo(({ version, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const { AppAdditionalInfoProductDetails: strings } = useAppStrings();

  const releaseDateLocaleFormatted = useDateInfo({
    dateString: version.releaseDate,
  })?.localeFormatted;

  const lastModifiedDateLocaleFormatted = useDateInfo({
    dateString: version.lastModified,
  })?.localeFormatted;

  const formattedVersionNumber = version.versionNumber
    .split(".")
    .map((number) => formatNumber({ localeCode, number: parseInt(number) }))
    .join(".");

  // TODO: Restore version size and checksum display (maybe via new fields on
  // VersionNode?)

  // const firstVersionCode = version.versionCodes.edges[0]?.node;

  // const firstVersionCodeSizeFormatted = firstVersionCode
  //   ? formatByte({ localeCode, number: firstVersionCode.size ?? 0 })
  //   : null;

  return (
    <li {...remainingProps}>
      <h2 css={paragraphP2SemiBold}>{strings.productDetails}</h2>
      <div>
        {releaseDateLocaleFormatted && (
          <p css={item}>
            <span>{strings.releaseDate}: </span>
            <span>{releaseDateLocaleFormatted}</span>
          </p>
        )}
        {lastModifiedDateLocaleFormatted && (
          <p css={item}>
            <span>{strings.latestUpdate}: </span>
            <span>{lastModifiedDateLocaleFormatted}</span>
          </p>
        )}
        {formattedVersionNumber && (
          <p css={item}>
            <span>{strings.version}: </span>
            <span>{formattedVersionNumber}</span>
          </p>
        )}
        {/* {firstVersionCodeSizeFormatted && (
          <p css={item}>
            <span>{strings.size}: </span>
            <span>{firstVersionCodeSizeFormatted}</span>
          </p>
        )}
        {firstVersionCode?.checksum && (
          <p css={item}>
            <span>{strings.checksum}: </span>
            <span>{firstVersionCode.checksum}</span>
          </p>
        )} */}
      </div>
    </li>
  );
});

AppAdditionalInfoProductDetails.displayName = "AppAdditionalInfoProductDetails";

export default AppAdditionalInfoProductDetails;
