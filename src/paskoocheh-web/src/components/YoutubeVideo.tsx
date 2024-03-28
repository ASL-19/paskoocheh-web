import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

const container = css({
  "::after": {
    content: `" "`,
    display: "block",

    paddingBottom: "52.3438%",
  },
  maxWidth: "37.5rem",
  position: "relative",
});

const frame = css({
  border: "none",
  borderRadius: "1rem",
  height: "100%",
  left: "0",
  position: "absolute",
  top: "0",
  width: "100%",
});

const YoutubeVideo: StylableFC<{ video: string }> = memo(
  ({ className, video }) => {
    return (
      <div className={className} css={container}>
        <iframe
          allowFullScreen
          css={frame}
          // src={`https://www.youtube-nocookie.com/embed/${videoInfo.videoCode}`}\
          src={video}
          title={video}
        />
      </div>
    );
  },
);

YoutubeVideo.displayName = "YoutubeVideo";

export default YoutubeVideo;
