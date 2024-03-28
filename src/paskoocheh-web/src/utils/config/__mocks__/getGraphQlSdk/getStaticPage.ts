import {
  GqlGetStaticPage,
  GqlGetStaticPageVariables,
} from "src/generated/graphQl";
import staticPageTestDataBySlug from "src/test/data/staticPageTestDataBySlug";

const getStaticPage = (
  variables: GqlGetStaticPageVariables,
): Promise<GqlGetStaticPage> => {
  if (global?.graphQlSdkOverrides?.getStaticPageResponse) {
    return Promise.resolve(global.graphQlSdkOverrides.getStaticPageResponse);
  }

  return Promise.resolve({
    staticPage: staticPageTestDataBySlug[variables.staticPageSlug] ?? null,
  });
};

export default getStaticPage;
