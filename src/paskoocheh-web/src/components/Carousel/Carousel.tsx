import "keen-slider/keen-slider.min.css";

import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import {
  KeenSliderHooks,
  KeenSliderOptions,
  useKeenSlider,
} from "keen-slider/react";
import { cloneElement, memo, ReactElement, useCallback, useState } from "react";

import CarouselArrow from "src/components/Carousel/CarouselArrow";
import { useAppLocaleInfo } from "src/stores/appStore";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type CarouselStrings = {
  /**
   * Label text that shows the description of the `>` arrow button for
   * accessibility purposes
   */
  a11yNextButtonLabel: string;
  /**
   * Label text that shows the description of the `<` arrow button for
   * accessibility purposes
   */
  a11yPreviousButtonLabel: string;
};

const container = ({ itemHeight }: { itemHeight: string }) =>
  css({
    display: "flex",
    flexDirection: "column",
    gap: "2rem",
    /* Reduce layout shift when carousel loads */
    "html.js": {
      /* 2rem = gap, 1rem = dots */
      height: `calc(${itemHeight} + 2rem + 1rem)`,
    },
    position: "relative",
    width: "100%",
  });

const slider = ({ sliderIsLoaded }: { sliderIsLoaded: boolean }) =>
  css({
    "html.js": {
      visibility: sliderIsLoaded ? "visible" : "hidden",
    },
  });

const arrow = css({
  alignItems: "center",
  background: colors.neutral50,
  borderRadius: "100%",
  boxShadow: "rgba(0, 0, 0, 0.35) 0px 5px 15px",
  display: "flex",
  height: "2.5rem",
  justifyContent: "center",
  opacity: "0.8",
  position: "absolute",
  top: "50%",
  transform: "translateY(-50%)",
  width: "2.5rem",
});

const arrowPrevious = css(
  arrow,
  {
    insetInlineStart: "-1.25rem",
  },
  breakpointStyles({
    desktopFull: {
      lt: {
        insetInlineStart: "-0.75rem",
      },
    },
  }),
);

const arrowNext = css(
  arrow,
  {
    insetInlineEnd: "-1.25rem",
  },
  breakpointStyles({
    desktopFull: {
      lt: {
        insetInlineEnd: "-0.75rem",
      },
    },
  }),
);

const Carousel: StylableFC<{
  itemHeight: string;
  keenSliderOptions: Pick<
    KeenSliderOptions<{}, {}, KeenSliderHooks>,
    "breakpoints" | "slides"
  >;
  slideElements: Array<ReactElement>;
}> = memo(({ className, itemHeight, keenSliderOptions, slideElements }) => {
  const { direction } = useAppLocaleInfo();

  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [maxSlideIndex, setMaxSlideIndex] = useState(0);
  const [sliderIsLoaded, setSliderIsLoaded] = useState(false);

  const pageIndexes = Array.from({
    length: Math.ceil(slideElements.length),
  }).map((value, index) => index);

  const currentPageIndex = Math.ceil(currentSlideIndex);

  const [sliderElementRef, sliderRef] = useKeenSlider<HTMLDivElement>({
    created: () => {
      // Don’t show slider until layout is complete (use setTimeout to wait a
      // "tick" for Keen to finish layout).
      setTimeout(() => {
        setSliderIsLoaded(true);
      }, 0);
    },
    detailsChanged(slider) {
      setMaxSlideIndex(slider.track.details.maxIdx);
    },
    renderMode: "performance",
    rtl: direction === "rtl",
    slideChanged(slider) {
      setCurrentSlideIndex(slider.track.details.rel);
    },
    ...keenSliderOptions,
  });

  const prevArrowIsEnabled = currentPageIndex > 0;
  const nextArrowIsEnabled = currentPageIndex < pageIndexes.length - 1;

  const onPrevArrowClick = useCallback(() => {
    if (prevArrowIsEnabled) {
      sliderRef.current?.moveToIdx((currentPageIndex - 1) * 1);
    }
  }, [currentPageIndex, prevArrowIsEnabled, sliderRef]);

  const onNextArrowClick = useCallback(() => {
    if (nextArrowIsEnabled) {
      const index =
        currentPageIndex + 2 > slideElements.length
          ? slideElements.length - 1
          : currentPageIndex + 1;

      sliderRef.current?.moveToIdx(index);
    }
  }, [currentPageIndex, nextArrowIsEnabled, slideElements.length, sliderRef]);

  const slideElementsWithKeenClassName = slideElements.map((slideElement) =>
    cloneElement(slideElement, {
      className: `${
        slideElement.props.className || ""
      } keen-slider__slide`.trim(),
    }),
  );

  return (
    <div className={className} css={container({ itemHeight })}>
      <div
        className="keen-slider"
        css={slider({ sliderIsLoaded })}
        ref={sliderElementRef}
      >
        {slideElementsWithKeenClassName}
      </div>

      {sliderIsLoaded && sliderRef.current && (
        <>
          {currentSlideIndex > 0 && (
            <CarouselArrow
              ariaLabel={"strings.a11yPreviousButtonLabel"}
              css={arrowPrevious}
              direction="back"
              isEnabled={prevArrowIsEnabled}
              onClick={onPrevArrowClick}
            />
          )}

          {currentSlideIndex < maxSlideIndex && (
            <CarouselArrow
              ariaLabel={"strings.a11yNextButtonLabel"}
              css={arrowNext}
              direction="forward"
              isEnabled={nextArrowIsEnabled}
              onClick={onNextArrowClick}
            />
          )}
        </>
      )}
    </div>
  );
});

Carousel.displayName = "Carousel";

export default Carousel;
