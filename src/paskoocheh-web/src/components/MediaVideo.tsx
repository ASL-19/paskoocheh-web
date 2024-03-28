import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type AppHowToUseStrings = {
  howToUse: string;
  introduction: string;
};

const container = css({
  // aspectRatio: "16/9",
  backgroundColor: colors.shadesBlack,
  borderRadius: "1rem",
  height: "fit-content",
  maxWidth: "37.5rem",
  width: "100%",
});

const MediaVideo: StylableFC<{ video: string }> = memo(({ video }) => {
  const strings = useAppStrings();

  return (
    // eslint-disable-next-line jsx-a11y/media-has-caption
    <video
      controls
      css={container}
      // Some browsers may use height and width to automatically set the aspect
      // ratio (like they do with img elements now)
      preload="metadata"
    >
      <source
        src={`${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${video}`}
        type="video/mp4"
      />

      {strings.shared.errorMessages.videoError}
    </video>
  );
});

MediaVideo.displayName = "MediaVideo";

export default MediaVideo;
