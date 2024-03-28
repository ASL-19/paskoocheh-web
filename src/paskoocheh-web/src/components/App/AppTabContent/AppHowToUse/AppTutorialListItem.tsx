import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";
import { match, P } from "ts-pattern";

import MediaVideo from "src/components/MediaVideo";
import YoutubeVideo from "src/components/YoutubeVideo";
import { GqlTutorial } from "src/generated/graphQl";
import { paragraphP2SemiBold } from "src/styles/typeStyles";

const container = css(paragraphP2SemiBold, {
  display: "flex",
  flexDirection: "column",
  rowGap: "1.25rem",
});

const AppTutorialListItem: StylableFC<{
  tutorial: GqlTutorial;
}> = memo(({ className, tutorial }) => {
  return (
    <div className={className} css={container}>
      <h2>{tutorial.title}</h2>
      {match(tutorial)
        .with({ video: P.string }, (tutorial) => (
          <MediaVideo video={tutorial.video ?? ""} />
        ))
        .with({ videoLink: P.string }, (tutorial) => (
          <YoutubeVideo video={tutorial.videoLink} />
        ))
        .otherwise(() => null)}
      ;
    </div>
  );
});

AppTutorialListItem.displayName = "AppTutorialListItem";

export default AppTutorialListItem;
