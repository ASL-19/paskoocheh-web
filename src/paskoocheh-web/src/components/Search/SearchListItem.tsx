import { ComboboxItem } from "@ariakit/react/combobox";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import Link from "next/link";
import { memo, useMemo } from "react";

import StarSvg from "src/components/icons/general/StarSvg";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo } from "src/stores/appStore";
import { dropdownBackgroundWhenActiveItem } from "src/styles/dropdownStyles";
import { ValidVersionPreview } from "src/types/appTypes";
import colors from "src/values/colors";

const container = css(dropdownBackgroundWhenActiveItem, {
  alignItems: "flex-start",
  columnGap: "1rem",
  display: "flex",
  flexDirection: "row",
  padding: "0 1.5rem",
});

const ratingContainer = css({
  alignItems: "center",
  columnGap: "0.5rem",
  display: "flex",
  flexDirection: "row",
});

const img = css({
  alignSelf: "center",
  borderRadius: "0.5rem",
  height: "2.5rem",
  width: "2.5rem",
});

const placeholderLogo = css({
  alignSelf: "center",
  background: "salmon",
  borderRadius: "0.5rem",
  height: "2.5rem",
  width: "2.5rem",
});

const nameText = css({
  color: colors.secondary500,
});

const ratingText = css({
  color: colors.neutral800,
});

const starIcon = css({
  color: colors.neutral800,
  height: "1rem",
  width: "1rem",
});

// ==============================
// ===== Next.js component ======
// ==============================
const SearchListItem: StylableFC<{
  versionPreview: ValidVersionPreview;
}> = memo(({ versionPreview, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();

  const slug = versionPreview.tool.slug;

  const firstLogo = versionPreview.tool?.images?.find(
    (image) => image?.imageType === "logo",
  );
  const imagePath = firstLogo
    ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${firstLogo?.image}`
    : "";

  const link = useMemo(
    () => (
      <Link
        href={routeUrls.app({
          localeCode,
          platform: versionPreview.platform.slugName,
          slug,
          toolType:
            versionPreview.tool?.primaryTooltype?.slug ||
            versionPreview.tool.toolTypes[0].slug,
        })}
      />
    ),
    [localeCode, slug, versionPreview],
  );

  return (
    <ComboboxItem
      render={link}
      css={container}
      focusOnHover
      value={versionPreview.tool?.name}
      key={versionPreview.id}
      {...remainingProps}
    >
      {imagePath && (
        <Image
          src={imagePath}
          key={firstLogo?.pk}
          alt={versionPreview.tool?.name}
          css={img}
          width={firstLogo?.width ?? 100}
          height={firstLogo?.height ?? 100}
        />
      )}

      {!imagePath && <div css={placeholderLogo} />}
      <div>
        <span css={nameText}>{versionPreview.tool?.name}</span>
        <div css={ratingContainer}>
          <span css={ratingText}>
            {versionPreview.averageRating?.starRating}
          </span>{" "}
          <StarSvg css={starIcon} />
        </div>
      </div>
    </ComboboxItem>
  );
});

SearchListItem.displayName = "SearchListItem";

export default SearchListItem;
