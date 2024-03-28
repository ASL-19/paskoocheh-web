import { StylableFC } from "@asl-19/react-dom-utils";
import { css, SerializedStyles } from "@emotion/react";
import Image from "next/image";
import { memo, useMemo } from "react";

import StarSvg from "src/components/icons/general/StarSvg";
import LinkOverlay from "src/components/LinkOverlay";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import {
  captionRegular,
  paragraphP1Regular,
  paragraphP1SemiBold,
  paragraphP2SemiBold,
} from "src/styles/typeStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import { HeadingLevel, HeadingTagName } from "src/types/miscTypes";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";
import { breakpointStyles } from "src/utils/media/media";
import { threeColumnGridContainerImageSizes } from "src/values/layoutValues";

const container = css(
  {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    minWidth: "10rem",
    position: "relative",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        gap: "0.5rem",
      },
    },
  }),
);
const promoImage = css(
  {
    borderRadius: "0.5rem",
    objectFit: "cover",
    width: "100%",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        aspectRatio: "1/1",
      },
    },
  }),
);

const promoImageContainer = css(
  {
    aspectRatio: "9/4",
    background: "salmon",
    borderRadius: "0.5rem",
    objectFit: "cover",
    position: "relative",
    width: "100%",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        aspectRatio: "1/1",
      },
    },
  }),
);
const appInfo = css({
  display: "flex",
  gap: "1rem",
});
const appDetails = css(
  {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    overflow: "hidden",
    rowGap: "0.25rem",
  },
  paragraphP1Regular,
  breakpointStyles({
    singleColumn: {
      lt: captionRegular,
    },
  }),
);

const logo = css({
  borderRadius: "100%",
  flex: "0 0 auto",
  height: "4rem",
  width: "4rem",
});

const placeholderLogo = css({
  background: "red",
  borderRadius: "100%",
  flex: "0 0 auto",
  height: "4rem",
  width: "4rem",
});

const overflowHidden = css({
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
});

const name = css(
  paragraphP2SemiBold,
  overflowHidden,
  breakpointStyles({
    singleColumn: {
      lt: paragraphP1SemiBold,
    },
  }),
);

const rating = css(overflowHidden, {
  alignItems: "center",
  display: "flex",
  gap: "0.25rem",
  height: "1.0625rem",
});
const icon = css({
  height: "1rem",
  width: "1rem",
});

export const getAppListItemElementId = (appPreview: ValidVersionPreview) =>
  `AppPreviewListItem-${appPreview.id}`;

const AppListItem: StylableFC<{
  hasLogo?: boolean;
  hasPromoImage?: boolean;
  headingLevel: HeadingLevel;
  logoCss?: SerializedStyles;
  versionPreview: ValidVersionPreview;
}> = memo(
  ({
    className,
    hasLogo = true,
    hasPromoImage = false,
    headingLevel,
    logoCss,
    versionPreview,
  }) => {
    const HeadingTag = `h${headingLevel}` as HeadingTagName;
    const { localeCode } = useAppLocaleInfo();

    const logoCssCombined = useMemo(() => css(logo, logoCss), [logoCss]);

    const primaryToolType = getValidToolPrimaryToolType(versionPreview.tool);

    const appUrl = routeUrls.app({
      localeCode,
      platform: versionPreview.platform.slugName,
      slug: versionPreview.tool.slug,
      toolType: primaryToolType.slug,
    });

    const firstLogoImagePath = useMemo(() => {
      const firstLogoImage = versionPreview.tool.images?.find(
        (image) => image?.imageType === "logo",
      );

      return firstLogoImage
        ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${firstLogoImage.image}`
        : null;
    }, [versionPreview.tool.images]);

    const firstHeaderImagePath = useMemo(() => {
      const promoImg = versionPreview.tool.images?.find(
        (img) => img?.imageType === "header",
      );

      return promoImg
        ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${promoImg.image}`
        : null;
    }, [versionPreview.tool.images]);

    return (
      <li className={className} css={container}>
        {hasPromoImage &&
          (firstHeaderImagePath ? (
            <div css={promoImageContainer}>
              <Image
                src={firstHeaderImagePath}
                fill
                css={promoImage}
                sizes={threeColumnGridContainerImageSizes}
                alt=""
              />
            </div>
          ) : (
            <div aria-hidden css={promoImageContainer} />
          ))}

        <div css={appInfo}>
          {hasLogo && firstLogoImagePath ? (
            <Image
              src={firstLogoImagePath}
              width="100"
              height="100"
              alt=""
              css={logoCssCombined}
            />
          ) : (
            <div aria-hidden css={placeholderLogo} />
          )}

          <div css={appDetails}>
            <HeadingTag css={name}>{versionPreview.tool.name}</HeadingTag>

            <p>{primaryToolType.name}</p>

            <p css={rating}>
              {versionPreview.averageRating &&
                versionPreview.averageRating.starRating !== 0 && (
                  <>
                    {versionPreview.averageRating.starRating}

                    <StarSvg css={icon} />
                  </>
                )}
            </p>
          </div>
        </div>
        <LinkOverlay url={appUrl} />
      </li>
    );
  },
);

AppListItem.displayName = "AppListItem";

export default AppListItem;
