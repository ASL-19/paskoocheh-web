import { NextPage } from "next";

import { Strings } from "src/types/stringTypes";

type LocalePageComponentStaticProperties = {
  strings: Strings;
};

const createLocalePageComponent = ({
  pageComponent,
  strings,
}: {
  pageComponent: NextPage;
} & LocalePageComponentStaticProperties) => {
  const localePage = (
    process.env.NODE_ENV !== "development" || !process.browser
      ? pageComponent.bind({})
      : pageComponent
  ) as NextPage & LocalePageComponentStaticProperties;

  localePage.displayName = pageComponent.name;
  localePage.strings = strings;

  return localePage;
};

export default createLocalePageComponent;
