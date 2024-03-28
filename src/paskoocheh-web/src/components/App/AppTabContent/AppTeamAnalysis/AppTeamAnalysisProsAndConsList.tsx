import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import { paragraphP2Regular, paragraphP2SemiBold } from "src/styles/typeStyles";

const item = css(paragraphP2Regular, {
  display: "flex",
  flexDirection: "column",
  padding: "1rem",
  rowGap: "1rem",
});

const text = ({ colorCss }: { colorCss: string }) =>
  css(paragraphP2SemiBold, {
    color: colorCss,
  });

const AppTeamAnalysisProsAndConsList: StylableFC<{
  colorCss: string;
  reviews: string;
  title: string;
}> = memo(({ colorCss, reviews, title }) => (
  <div>
    <h3 css={text({ colorCss })}>{title}</h3>
    <p css={item}>{reviews}</p>
  </div>
));

AppTeamAnalysisProsAndConsList.displayName = "AppTeamAnalysisProsAndConsList";

export default AppTeamAnalysisProsAndConsList;
