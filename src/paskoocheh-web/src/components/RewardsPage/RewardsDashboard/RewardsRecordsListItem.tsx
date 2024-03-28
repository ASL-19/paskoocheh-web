import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";
import { match } from "ts-pattern";

import FormattedDate from "src/components/FormattedDate";
import { GqlRewardRecord } from "src/generated/graphQl";
import useDateInfo from "src/hooks/useDateInfo";
import { useAppStrings } from "src/stores/appStore";
import { dashboardItemHeadingAndDescription } from "src/styles/dashboardStyles";
import {
  captionRegular,
  captionSemiBold,
  paragraphP2Regular,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css({
  borderBottom: `1px solid ${colors.secondary50}`,
  display: "flex",
  justifyContent: "space-between ",
  padding: "1rem 0",
});

const points = css(
  paragraphP2SemiBold,
  breakpointStyles({ singleColumn: { lt: captionSemiBold } }),
);

const pointsEarned = css(points, {
  color: colors.success500,
});

const pointsRedeemed = css(points, {
  color: colors.error500,
});

const action = css(
  paragraphP2Regular,
  breakpointStyles({ singleColumn: { lt: captionSemiBold } }),
);
const date = css(captionRegular, {
  color: colors.secondary400,
});

const RewardsRecordsListItem: StylableFC<{ record: GqlRewardRecord }> = memo(
  ({ className, record }) => {
    const { RewardsPageContent: strings } = useAppStrings();

    const dateInfo = useDateInfo({
      dateString: record.date,
    });

    return (
      <li className={className} css={container}>
        <div css={dashboardItemHeadingAndDescription}>
          <p css={action}>{record.description}</p>
          {dateInfo && <FormattedDate dateInfo={dateInfo} css={date} />}
        </div>

        {match(record.recordType)
          .with("EARNED", () => (
            <div css={pointsEarned}>
              +&nbsp;{record.points}&nbsp;{strings.points}
            </div>
          ))
          .with("REDEEMED", () => (
            <div css={pointsRedeemed}>
              -&nbsp;{record.points}&nbsp;{strings.points}
            </div>
          ))
          .exhaustive()}
      </li>
    );
  },
);

RewardsRecordsListItem.displayName = "RewardsRecordsListItem";

export default RewardsRecordsListItem;
