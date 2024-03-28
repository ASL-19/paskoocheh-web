/* eslint-disable @mizdra/layout-shift/require-size-attributes */
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import { ComponentProps, memo, useMemo } from "react";

import Carousel from "src/components/Carousel/Carousel";
import PageSegment from "src/components/Page/PageSegment";
import { ValidToolImage } from "src/types/appTypes";

const itemHeight = "23.5rem";

const container = css({
  padding: "3.25rem 0",
});

const item = css({
  display: "block",
  flex: "0 0 auto",
  height: "23.5rem",
  maxWidth: "100%",
  width: "auto !important",
});

const image = css({
  borderRadius: "0.5rem",
  height: "100%",
  objectFit: "contain",
  width: "100%",
});

const AppScreenshots: StylableFC<{
  validToolImages: Array<ValidToolImage>;
}> = memo(({ validToolImages }) => {
  const carouselProps: ComponentProps<typeof Carousel> = useMemo(
    () => ({
      itemHeight,
      keenSliderOptions: {
        slides: {
          perView: "auto",
          spacing: 16,
        },
      },
      slideElements: validToolImages.map((validToolImage) => (
        <li
          css={item}
          style={{
            aspectRatio: validToolImage.width / validToolImage.height,
          }}
          key={validToolImage.id}
        >
          <Image
            src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${validToolImage.image}`}
            alt=""
            width={validToolImage.width}
            height={validToolImage.height}
            css={image}
          />
        </li>
      )),
    }),
    [validToolImages],
  );

  return (
    <PageSegment as="section" css={container}>
      {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex */}
      <Carousel {...carouselProps} />
    </PageSegment>
  );
});

AppScreenshots.displayName = "AppScreenshots";

export default AppScreenshots;
