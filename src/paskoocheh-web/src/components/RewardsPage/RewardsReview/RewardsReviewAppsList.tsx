import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import RewardsReviewAppsListItem from "src/components/RewardsPage/RewardsReview/RewardsReviewAppsListItem";
import { ValidVersionPreview } from "src/types/appTypes";

const container = css({ width: "100%" });

const RewardsReviewAppsList: StylableFC<{
  type: "notYetReviewed" | "reviewed";
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(({ type, versionPreviews, ...remainingProps }) => (
  <div css={container} {...remainingProps}>
    {versionPreviews?.map((versionPreview) => (
      <RewardsReviewAppsListItem
        versionPreview={versionPreview}
        key={versionPreview.id}
        type={type}
      />
    ))}
  </div>
));

RewardsReviewAppsList.displayName = "RewardsReviewAppsList";

export default RewardsReviewAppsList;
