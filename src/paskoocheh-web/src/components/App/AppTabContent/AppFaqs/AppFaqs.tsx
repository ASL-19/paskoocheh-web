import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import AppFaqsListItem from "src/components/App/AppTabContent/AppFaqs/AppFaqsListItem";
import { GqlFaq } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";

export type AppFaqsStrings = {
  /**
   * Text for No Faq
   */
  noFaq: string;
};

const container = css({
  backgroundColor: colors.neutral50,
  borderRadius: "0.5rem",
  padding: "1.25rem",
});

const collapseContainer = css({
  "& > dt:first-of-type": {
    paddingTop: "0",
  },
  "& > dt:last-of-type": {
    paddingBottom: "0",
  },
  display: "flex",
  flexDirection: "column",
});

const AppFaqs: StylableFC<{ faqs: Array<GqlFaq> }> = memo(
  ({ faqs, ...remainingProps }) => {
    const { AppFaqs: strings } = useAppStrings();

    if (faqs.length === 0) return <div>{strings.noFaq}</div>;

    const sortedFaqs = faqs.sort((a, b) => (a.order ?? 0) - (b.order ?? 0));

    return (
      <div css={container} {...remainingProps}>
        <dl css={collapseContainer}>
          {sortedFaqs.map((faq) => (
            <AppFaqsListItem faq={faq} key={faq.id} />
          ))}
        </dl>
      </div>
    );
  },
);

AppFaqs.displayName = "AppFaqs";

export default AppFaqs;
