import { hoverStyles } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";
import { AriaAttributes, Dispatch, FC, memo, SetStateAction } from "react";

import StarSvg from "src/components/icons/general/StarSvg";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type StarRatingsStrings = {
  /**
   * Accessibility label for rating star when clicking a new rating.
   *
   * \{rating\} is replaced by the star’s rating number (1/2/3/4/5)
   */
  setRatingAriaLabel: string;

  /**
   * Accessibility label for rating star when clicking the current rating’s star
   * to unset the rating.
   */
  unsetRatingAriaLabel: string;
};

// ==============
// === Styles ===
// ==============
const container = ({ disabled }: { disabled: boolean }) =>
  css(
    {
      alignItems: "center",
      display: "flex",
      pointerEvents: disabled ? "none" : "auto",
    },
    hoverStyles({
      button: {
        color: `${colors.secondary300}`,
      },
    }),
  );

const starButton = ({
  fillColor,
  isSelected,
}: {
  fillColor: string;
  isSelected: boolean;
}) =>
  css(
    {
      color: isSelected ? fillColor : colors.neutral200,
      cursor: "pointer",
      padding: "0.25rem",
    },
    // Via https://stackoverflow.com/a/29530752
    hoverStyles({
      "~ button": {
        color: colors.neutral200,
      },
    }),
  );

const ratingStar = css({
  display: "block",
  height: "2rem",
  width: "2rem",
});

// ==============================
// ===== Next.js component ======
// ==============================
const StarRatings: FC<{
  // We could set the aria-labelledby prop directly but we’d have to remember to
  // pass it into the <div> props (e.g. by spreading the remaining props), which
  // is error-prone.
  ariaLabelledBy?: AriaAttributes["aria-labelledby"];
  className?: string;
  disabled?: boolean;
  fillColor?: string;
  rating: number;
  setRating: Dispatch<SetStateAction<number>>;
}> = memo(
  ({
    ariaLabelledBy,
    className,
    disabled = false,
    fillColor,
    rating,
    setRating,
  }) => {
    const strings = useAppStrings();

    return (
      <div
        aria-labelledby={ariaLabelledBy}
        className={className}
        css={container({ disabled })}
      >
        {[1, 2, 3, 4, 5].map((starRating) => {
          const isCurrentRating = rating === starRating;

          return (
            <button
              css={starButton({
                fillColor: fillColor || colors.secondary500,
                isSelected: isCurrentRating || rating > starRating,
              })}
              className="starButton"
              key={starRating}
              type="button"
              disabled={disabled}
              aria-label={
                isCurrentRating
                  ? strings.StarRatings.unsetRatingAriaLabel
                  : strings.StarRatings.setRatingAriaLabel.replace(
                      "{rating}",
                      `${starRating}`,
                    )
              }
              onClick={() => {
                isCurrentRating ? setRating(0) : setRating(starRating);
              }}
            >
              <StarSvg css={ratingStar} />
            </button>
          );
        })}
      </div>
    );
  },
);

StarRatings.displayName = "StarRatings";

export default StarRatings;
