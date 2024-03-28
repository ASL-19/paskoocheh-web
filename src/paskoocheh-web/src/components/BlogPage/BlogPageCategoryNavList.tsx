import { StylableFC } from "@asl-19/react-dom-utils";
import { memo, useMemo } from "react";

import CategoryNavList from "src/components/CategoryNavList";
import { GqlTopic } from "src/generated/graphQl";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { RouteInfo } from "src/types/miscTypes";

const BlogPageCategoryNavList: StylableFC<{
  topics: Array<GqlTopic>;
}> = memo(({ topics, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const routeInfos = useMemo<Array<RouteInfo>>(
    () => [
      {
        key: "all",
        name: strings.shared.all,
        route: routeUrls.blog({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
        }),
      },
      ...topics.map((routeInfo) => ({
        key: routeInfo.name,
        name: routeInfo.name,
        route: routeUrls.blog({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          topic: routeInfo.slug,
        }),
      })),
    ],
    [localeCode, queryOrDefaultPlatformSlug, strings.shared.all, topics],
  );

  return (
    <CategoryNavList
      activeUrlComparisonQueryKeys={useMemo(() => ["topic"], [])}
      routeInfos={routeInfos}
      shallow
      {...remainingProps}
    />
  );
});

BlogPageCategoryNavList.displayName = "BlogPageCategoryNavList";

export default BlogPageCategoryNavList;
