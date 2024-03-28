import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, useMemo } from "react";

import CategoryNavList from "src/components/CategoryNavList";
import { GqlToolType } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { RouteInfo } from "src/types/miscTypes";
import getLocaleToolTypeName from "src/utils/getLocaleToolTypeName";

const HomePageCategoryNavList: StylableFC<{
  toolTypes: Array<GqlToolType>;
}> = memo(({ toolTypes, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const routeInfos = useMemo<Array<RouteInfo>>(
    () => [
      {
        key: "all",
        name: strings.shared.all,
        route: routeUrls.home({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
      },
      ...toolTypes.map((toolType) => ({
        key: toolType.name,
        name: getLocaleToolTypeName({ localeCode, toolType }),
        route: routeUrls.home({
          category: toolType.slug,
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
      })),
    ],
    [localeCode, queryOrDefaultPlatformSlug, strings.shared.all, toolTypes],
  );

  return (
    <CategoryNavList
      activeUrlComparisonQueryKeys={useMemo(() => ["category"], [])}
      routeInfos={routeInfos}
      shallow
      {...remainingProps}
    />
  );
});

HomePageCategoryNavList.displayName = "HomePageCategoryNavList";

export default HomePageCategoryNavList;
