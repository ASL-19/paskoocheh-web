import { hoverStyles } from "@asl-19/emotion-utils";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { useRouter } from "next/router";
import { memo } from "react";
import { match } from "ts-pattern";

import ButtonButton from "src/components/ButtonButton";
import ButtonLink from "src/components/ButtonLink";
import LoadingIndicatorSvg from "src/components/icons/animation/LoadingIndicatorSvg";
import NoResultsIllustrationAndMessage from "src/components/NoResultsIllustrationAndMessage";
import { IndexPageLoadingState } from "src/hooks/useIndexPageLoadingAndQueryLogic";
import { useAppStrings } from "src/stores/appStore";
import colors from "src/values/colors";
import { buttonHeights } from "src/values/layoutValues";

export type IndexPageLoadingUiStrings = {
  errorMessage: string;
  errorReloadButtonText: string;
};

const loadMoreButtonClassName = "loadMoreButton";

const wrapper = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
});

const text = css({
  color: colors.primary500,
});

const buttonLink = css(
  {
    backgroundColor: "transparent",
    boxShadow: "0 0 0 0",
    padding: "0 3.75rem",
  },
  hoverStyles({
    backgroundColor: "transparent",
  }),
);

const loadingInitialIndicator = css({
  height: "8rem",
});

const loadingMoreIndicator = css({
  height: buttonHeights.medium,
  transform: "scale(1.5)",
});

/**
 * Index page “load more” link, loading indicator, “no results” message, or
 * error message.
 *
 * Rendered element corresponds to IndexPageLoadingState
 */
const IndexPageLoadingUi: StylableFC<{
  buttonType?: "link" | "button";
  loadMoreLinkHref?: string;
  loadMoreLinkText: string;
  loadingState: IndexPageLoadingState;
  onClick?: () => void;
}> = memo(
  ({
    buttonType = "link",
    className,
    loadMoreLinkHref = "",
    loadMoreLinkText,
    loadingState,
    onClick,
  }) => {
    const router = useRouter();

    const { IndexPageLoadingUi: strings } = useAppStrings();
    return match(loadingState)
      .with({ type: "error" }, () => (
        <div className={className} css={wrapper}>
          <p>{strings.errorMessage}</p>

          <ButtonLink
            css={buttonLink}
            href={router.asPath}
            replace
            scroll={false}
            shallow
            text={strings.errorReloadButtonText}
            variant="secondary"
          />
        </div>
      ))
      .with({ type: "hasMore" }, () => (
        <div className={className} css={wrapper}>
          {buttonType === "link" ? (
            <ButtonLink
              className={loadMoreButtonClassName}
              css={buttonLink}
              href={loadMoreLinkHref}
              replace
              scroll={false}
              shallow
              text={loadMoreLinkText}
              textCss={text}
              variant="secondary"
            />
          ) : (
            <ButtonButton
              className={loadMoreButtonClassName}
              css={buttonLink}
              text={loadMoreLinkText}
              textCss={text}
              variant="secondary"
              onClick={onClick}
            />
          )}
        </div>
      ))
      .with({ type: "hasNoMore" }, () => null)
      .with({ type: "hasNone" }, () => (
        <NoResultsIllustrationAndMessage className={className} />
      ))
      .with({ type: "loadingNew" }, () => (
        <div className={className} css={wrapper}>
          <LoadingIndicatorSvg css={loadingInitialIndicator} />
        </div>
      ))
      .with({ type: "loadingMore" }, () => (
        <div className={className} css={wrapper}>
          <LoadingIndicatorSvg css={loadingMoreIndicator} />
        </div>
      ))
      .exhaustive();
  },
);

IndexPageLoadingUi.displayName = "IndexPageLoadingUi";

export default IndexPageLoadingUi;
