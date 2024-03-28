import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import { memo } from "react";
import { match } from "ts-pattern";

import { GqlVersionPreview } from "src/generated/graphQl";
import { useAppLocaleInfo } from "src/stores/appStore";
import { captionSemiBold, paragraphP2SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";

const container = css({
  alignItems: "center",
  display: "flex",
  gap: "1.5rem",
  width: "100%",
});

const logo = css(
  {
    borderRadius: "100%",
    height: "4rem",
    width: "4rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        height: "2rem",
        width: "2rem",
      },
    },
  }),
);

const name = css(
  paragraphP2SemiBold,
  breakpointStyles({
    singleColumn: {
      lt: captionSemiBold,
    },
  }),
);

const SimpleAppInfo: StylableFC<{ versionPreview: GqlVersionPreview }> = memo(
  ({ className, versionPreview }) => {
    const { localeCode } = useAppLocaleInfo();

    const firstLogo = versionPreview.tool?.images?.find(
      (image) => image?.imageType === "logo",
    );
    const imagePath = firstLogo
      ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${firstLogo?.image}`
      : "";

    const localePlatformDisplayName = match(localeCode)
      .with("en", () => versionPreview.platform?.displayName)
      .with("fa", () => versionPreview.platform?.displayNameFa)
      .exhaustive();

    return (
      <div className={className} css={container}>
        <Image
          src={imagePath}
          alt=""
          css={logo}
          width={firstLogo?.width ?? 100}
          height={firstLogo?.height ?? 100}
        />
        <h2 css={name}>
          {/* Technically localePlatformDisplayName could be falsy but in
          practice it should always be set unless the editors have made a
          mistake */}
          {versionPreview.tool?.name} ({localePlatformDisplayName})
        </h2>
      </div>
    );
  },
);

SimpleAppInfo.displayName = "SimpleAppInfo";

export default SimpleAppInfo;
