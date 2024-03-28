import { lineClampedText } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css, SerializedStyles } from "@emotion/react";
import Image from "next/image";
import { memo } from "react";

import ButtonLink from "src/components/ButtonLink";
import PageSegment from "src/components/Page/PageSegment";
import { headingH1SemiBold, subheadingRegular } from "src/styles/typeStyles";
import { ButtonVariant } from "src/types/buttonTypes";
import { breakpointStyles } from "src/utils/media/media";
import { headerHeight } from "src/values/layoutValues";

const container = css({
  display: "flex",
  height: `calc(100vh - ${headerHeight})`,
  justifyContent: "center",
  maxHeight: "31.25rem",
  position: "relative",
  width: "100%",
});

const viewportImage = css({
  objectFit: "cover",
});

const contentImage = css({
  margin: "auto",
  maxHeight: "25rem",
  maxWidth: "1200px",
  objectFit: "cover",
  objectPosition: "90% 10%",
});

const overlayContainer = css(container, {
  left: 0,
  position: "absolute",
  top: "0",
});

const centeredContainer = ({ textColor }: { textColor: string }) =>
  css(
    {
      // This prevents the box from extending to the edges of the viewport if it
      // has a background image (to match the mobile design)
      // borderInline: backgroundImageUrl ? "1rem solid transparent" : undefined,
      color: textColor,
      display: "flex",
      flexDirection: "column",
      height: "100%",
      justifyContent: "center",
      maxHeight: "25rem",
      padding: "3rem",
      position: "relative",
      rowGap: "1.5rem",
      zIndex: 10,
    },
    breakpointStyles({
      desktopNarrow: {
        lt: {
          paddingInline: "1rem",
        },
      },
    }),
  );

const subHeader = css(
  subheadingRegular,

  lineClampedText({ fontSize: "1.25rem", lineCount: 2, lineHeight: 1.2 }),
);

const HomePagePromoBoxSegment: StylableFC<{
  buttonCss?: SerializedStyles;
  buttonText: string;
  buttonUrl: string;
  buttonVariant?: ButtonVariant;
  description: string;
  headingCss?: SerializedStyles;
  imageAlignment: "content" | "viewport";
  imageUrl: string;
  textColor: string;
  title: string;
}> = memo(
  ({
    buttonCss,
    buttonText,
    buttonUrl,
    buttonVariant = "primary",
    className,
    description,
    headingCss = headingH1SemiBold,
    imageAlignment,
    imageUrl,
    textColor,
    title,
  }) => (
    <div css={container}>
      <Image
        src={imageUrl}
        alt={description}
        priority
        sizes="100%"
        fill
        css={imageAlignment === "viewport" ? viewportImage : contentImage}
      />

      <div css={overlayContainer}>
        <PageSegment
          className={className}
          centeredContainerCss={centeredContainer({
            textColor,
          })}
          css={container}
        >
          <h2 css={headingCss}>{title}</h2>
          <p css={subHeader}>{description}</p>
          <ButtonLink
            css={buttonCss}
            text={buttonText}
            href={buttonUrl}
            variant={buttonVariant}
          />
        </PageSegment>
      </div>
    </div>
  ),
);

HomePagePromoBoxSegment.displayName = "HomePagePromoBoxSegment";

export default HomePagePromoBoxSegment;
