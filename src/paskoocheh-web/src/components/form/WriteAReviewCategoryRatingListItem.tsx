import { css } from "@emotion/react";
import { Dispatch, FC, memo, SetStateAction, useId } from "react";

import StarRatings from "src/components/form/StarRatings";
import { breakpointStyles } from "src/utils/media/media";

const listItem = css(
  {
    columnGap: "2rem",
    display: "flex",
    rowGap: "1rem",
  },
  breakpointStyles({
    singleColumn: {
      gte: {
        alignItems: "center",
        flexDirection: "row",
      },
      lt: {
        flexDirection: "column",
        justifyContent: "center",
      },
    },
  }),
);

const WriteAReviewCategoryRatingListItem: FC<{
  label: string;
  rating: number;
  setRating: Dispatch<SetStateAction<number>>;
}> = memo(({ label, rating, setRating }) => {
  const headingId = useId();

  return (
    <li css={listItem}>
      <h4 id={headingId}>{label}</h4>
      <StarRatings
        ariaLabelledBy={headingId}
        setRating={setRating}
        rating={rating}
      />
    </li>
  );
});

WriteAReviewCategoryRatingListItem.displayName =
  "WriteAReviewCategoryRatingListItem";

export default WriteAReviewCategoryRatingListItem;
