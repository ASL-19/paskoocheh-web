import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import StarSvg from "src/components/icons/general/StarSvg";
import useFormattedNumber from "src/hooks/useFormattedNumber";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { paragraphP1Regular, paragraphP2SemiBold } from "src/styles/typeStyles";
import { ValidVersion } from "src/types/appTypes";
import { Direction } from "src/types/layoutTypes";
import colors from "src/values/colors";

export type AppStatsDetailsStrings = {
  a11yLabel: string;
};

const list = css({
  display: "flex",
});

const item = ({ direction }: { direction: Direction }) =>
  css({
    "&:not(:last-child)::after": {
      borderColor: colors.secondary50,
      borderStyle: "solid",
      borderWidth: "1px",
      content: `""`,
      height: "1.875rem",
      left: direction === "rtl" ? "0" : "",
      position: "absolute",
      right: direction === "ltr" ? "0" : "",
      top: "50%",
      transform: "translateY(-50%)",
    },
    display: "flex",
    flex: "1",
    flexDirection: "column",
    position: "relative",
    rowGap: "0.5rem",
    textAlign: "center",
  });

const icon = css({
  fill: colors.secondary500,
  height: "1.25rem",
  width: "1.25rem",
});

const averageReview = css({
  alignItems: "center",
  columnGap: "0.35rem",
  display: "flex",
  justifyContent: "center",
});

const AppStatsDetails: StylableFC<{ version: ValidVersion }> = memo(
  ({ version, ...remainingProps }) => {
    const { direction } = useAppLocaleInfo();
    const strings = useAppStrings();

    const starRating = useFormattedNumber({
      decimalPoints: 1,
      number: version.averageRating?.starRating ?? 0,
    });

    const reviews = useFormattedNumber({
      number: version.averageRating?.ratingCount ?? 0,
    });

    const downloadCount = useFormattedNumber({
      number: version.downloadCount ?? 0,
    });

    return (
      <ul
        aria-label={strings.AppStatsDetails.a11yLabel}
        css={list}
        {...remainingProps}
      >
        <li css={item({ direction })}>
          <div css={averageReview}>
            <span css={paragraphP2SemiBold}>{starRating}</span>
            <StarSvg css={icon} />
          </div>
          <p css={paragraphP1Regular}>
            {`${reviews} ${strings.AppOverviewSection.reviews}`}
          </p>
        </li>
        <li css={item({ direction })}>
          <span css={paragraphP2SemiBold}>{downloadCount}</span>
          <p css={paragraphP1Regular}>{strings.AppOverviewSection.download}</p>
        </li>
      </ul>
    );
  },
);

AppStatsDetails.displayName = "AppStatsDetails";

export default AppStatsDetails;
