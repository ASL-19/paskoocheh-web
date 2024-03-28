import { css, SerializedStyles } from "@emotion/react";
import { FC, memo, useMemo } from "react";

import { HeadingLevel, HeadingTagName } from "src/types/miscTypes";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const headingWithIcon = css({
  color: colors.black,
  display: "flex",
  gridColumn: "span 16",
});

const headingIcon = css(
  {
    alignSelf: "center",
    fill: colors.blue,
    flex: "0 0 auto",
    height: "1.75rem",
    marginInlineEnd: "0.5rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: { display: "none" },
    },
  }),
);

const heading = css({ flex: "1 1 auto" });

const HeadingWithIcon: FC<{
  IconComponent: FC<{ className?: string }>;
  className?: string;
  headingCss?: SerializedStyles;
  headingId?: string;
  headingLevel: HeadingLevel;
  headingText: string;
}> = memo(
  ({
    IconComponent,
    className,
    headingCss,
    headingId,
    headingLevel,
    headingText,
  }) => {
    const HeadingTag = `h${headingLevel}` as HeadingTagName;

    const headingTagCss = useMemo(() => [heading, headingCss], [headingCss]);

    return (
      <div className={className} css={headingWithIcon}>
        <IconComponent aria-hidden css={headingIcon} />

        <div>
          <HeadingTag css={headingTagCss} id={headingId}>
            {headingText}
          </HeadingTag>
        </div>
      </div>
    );
  },
);
HeadingWithIcon.displayName = "HeadingWithIcon";

export default HeadingWithIcon;
