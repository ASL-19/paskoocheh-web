import { focusElement } from "@asl-19/js-dom-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import {
  memo,
  MouseEvent,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import HtmlContent from "src/components/HtmlContent";
import MinusSvg from "src/components/icons/general/MinusSvg";
import PlusSvg from "src/components/icons/general/PlusSvg";
import { GqlCollapsibleBlock } from "src/generated/graphQl";
import { paragraphP3SemiBold } from "src/styles/typeStyles";
import { SetNonNullable } from "src/types/utilTypes";
import colors from "src/values/colors";

const itemWrapper = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
  width: "100%",
});

const headingRow = css(paragraphP3SemiBold, {
  alignItems: "center",
  display: "flex",
  flexDirection: "row",
  gap: "0.5rem",
});

const headingText = css({
  color: colors.black,
  display: "block",
});

const detailsCollapsed = css(
  { display: "none" },
  {
    "html:not(.js) &": {
      display: "block",
    },
  },
);

const icon = css(
  {
    color: colors.black,
    height: "1rem",
    width: "1rem",
  },
  {
    "html:not(.js) &": {
      display: "none",
    },
  },
);

/**
 * A section of text which can be expanded and hidden.
 */
const CollapsibleBlock: StylableFC<{
  block: SetNonNullable<GqlCollapsibleBlock, "heading" | "slug" | "text">;
}> = memo(({ block, ...remainingProps }) => {
  const router = useRouter();
  const [isExpanded, setIsExpanded] = useState(false);

  const ddElement = useRef<HTMLElement>(null);

  const onClick = useCallback(
    (event: MouseEvent) => {
      event.preventDefault();

      setIsExpanded(!isExpanded);
    },
    [isExpanded],
  );

  useEffect(() => {
    if (isExpanded && ddElement.current) {
      focusElement(ddElement.current);
    }
  }, [isExpanded]);

  return (
    <div css={itemWrapper} {...remainingProps}>
      {/* The title */}
      <dt css={headingRow}>
        {isExpanded ? (
          <MinusSvg aria-hidden css={icon} />
        ) : (
          <PlusSvg aria-hidden css={icon} />
        )}
        <a
          css={headingText}
          href={`${router.asPath} #${block.slug} `}
          onClick={onClick}
        >
          {block.heading}
        </a>
      </dt>
      {/* The content to be expanded and collapsed */}
      <dd css={isExpanded ? undefined : detailsCollapsed} ref={ddElement}>
        <HtmlContent dangerousHtml={block.text} />
      </dd>
    </div>
  );
});

CollapsibleBlock.displayName = "CollapsibleBlock";

export default CollapsibleBlock;
