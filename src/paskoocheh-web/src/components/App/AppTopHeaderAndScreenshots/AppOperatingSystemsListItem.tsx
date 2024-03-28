import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Image from "next/image";
import Link from "next/link";
import { memo } from "react";

import { GqlPlatform, GqlTool } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { ValidVersion } from "src/types/appTypes";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";

const platformIconWidth = "2rem";

const platformIcon = css({
  height: "auto",
  width: platformIconWidth,
});

const platformIconInactive = css(platformIcon, {
  filter: "opacity(40%)",
});

const AppOperatingSystemsListItem: StylableFC<{
  currentPlatformVersion: ValidVersion;
  platform: GqlPlatform;
  tool: GqlTool;
}> = memo(({ currentPlatformVersion, platform, tool }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();

  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const isActive = queryOrDefaultPlatformSlug === platform.slugName;

  const platformIconUrl = `${process.env.NEXT_PUBLIC_BACKEND_URL}/media/${platform.icon}`;

  return (
    <li>
      <Link
        aria-current={isActive ? "page" : undefined}
        aria-label={strings.shared.operatingSystemsNames[platform.slugName]}
        href={routeUrls.app({
          localeCode,
          platform: platform.slugName,
          slug: tool.slug,
          toolType: getValidToolPrimaryToolType(currentPlatformVersion.tool)
            .slug,
        })}
      >
        <Image
          css={isActive ? platformIcon : platformIconInactive}
          src={platformIconUrl}
          width={100}
          height={100}
          // Will only be used if platformIconUrl isn’t an SVG (hopefully never!)
          sizes={platformIconWidth}
          alt=""
        />
      </Link>
    </li>
  );
});

AppOperatingSystemsListItem.displayName = "AppOperatingSystemsListItem";

export default AppOperatingSystemsListItem;
