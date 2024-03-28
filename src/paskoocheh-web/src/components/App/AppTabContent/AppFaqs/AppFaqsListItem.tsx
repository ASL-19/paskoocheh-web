import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { Fragment, memo, useCallback, useId, useState } from "react";

import HtmlContent from "src/components/HtmlContent";
import ChevronSvg from "src/components/icons/general/ChevronSvg";
import MediaVideo from "src/components/MediaVideo";
import { GqlDoIncrementClickCount, GqlFaq } from "src/generated/graphQl";
import { paragraphP1Regular } from "src/styles/typeStyles";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import colors from "src/values/colors";

const collapse = css(
  paragraphP1Regular,
  {
    padding: "1rem 0",
  },
  {
    "html:not(.js) &": {
      borderBottom: "none",
    },
  },
  {
    ":last-of-type": {
      borderBottom: "none",
    },
  },
);

const collapseOpen = css(collapse, {
  borderBottom: "none",
});

const collapseClosed = css(collapse, {
  borderBottom: `solid 1px ${colors.secondary50}`,
});

const faqQuestion = css({
  alignItems: "center",
  columnGap: "1rem",
  display: "flex",
  padding: "1rem 0",
  width: "100%",
});

const faqAnswerContent = ({ isOpen }: { isOpen: boolean }) =>
  css(
    {
      borderBottom: `solid 1px ${colors.secondary50}`,
      display: isOpen ? "block" : "none",
      paddingBottom: "1rem",
      position: "relative",
    },
    {
      "html:not(.js) &": {
        display: "block",
      },
    },
    {
      ":last-of-type": {
        borderBottom: "none",
      },
    },
  );

const chevron = css({
  fill: colors.shadesBlack,
  height: "1rem",
  minHeight: "1rem",
  minWidth: "1rem",
  width: "1rem",
});

const AppFaqsListItem: StylableFC<{
  faq: GqlFaq;
}> = memo(({ className, faq }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = useCallback(async () => {
    if (!isOpen) {
      setIsOpen(true);

      let incrementResponse: GqlDoIncrementClickCount;

      try {
        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        incrementResponse = await graphQlSdk.doIncrementClickCount({
          faqPk: faq.pk,
        });
      } catch (error) {
        console.error(
          "[AppFaqsListItem] Error while incrementing click count:",
          error,
        );
        return;
      }

      if (incrementResponse.incrementClickCount.errors) {
        console.error(
          "[AppFaqsListItem] Error(s) while incrementing click count:",
          incrementResponse.incrementClickCount.errors,
        );
      }
    } else {
      setIsOpen(false);
    }
  }, [faq.pk, isOpen]);

  const ddId = useId();

  return (
    <>
      <dt className={className} css={isOpen ? collapseOpen : collapseClosed}>
        <button
          aria-controls={ddId}
          aria-expanded={isOpen}
          css={faqQuestion}
          onClick={toggle}
        >
          <h2>{faq.headline}</h2>
          <ChevronSvg
            aria-hidden
            css={chevron}
            direction={isOpen ? "up" : "down"}
          />
        </button>
      </dt>

      <dd css={faqAnswerContent({ isOpen })} id={ddId}>
        <HtmlContent
          css={paragraphP1Regular}
          dangerousHtml={faq.body ?? ""}
        ></HtmlContent>
        {faq.video && <MediaVideo video={faq.video} />}
      </dd>
    </>
  );
});

AppFaqsListItem.displayName = "AppFaqsListItem";

export default AppFaqsListItem;
