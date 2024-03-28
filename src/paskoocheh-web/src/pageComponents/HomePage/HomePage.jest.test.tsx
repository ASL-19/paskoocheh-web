import { act } from "@testing-library/react";

import getHomePageServerSideProps from "src/pageComponents/HomePage/getHomePageServerSideProps";
import HomePage from "src/pageComponents/HomePage/HomePage";
import { AppProvider } from "src/stores/appStore";
import getMockAppState from "src/utils/jest/getMockAppState";
import getMockServerSidePropsArgs from "src/utils/jest/getMockServerSidePropsArgs";
import testRender from "src/utils/jest/testRender";
import { LocaleCode } from "src/values/localeValues";

["en", "fa"].forEach((localeCode: LocaleCode) => {
  const appState = getMockAppState({ localeCode });
  const { shared: sharedStrings } = appState.strings;

  test(`${localeCode} HomePage renders expected content`, async () => {
    const serverSideProps = await getHomePageServerSideProps({
      ...getMockServerSidePropsArgs(),
      params: {},
      query: {},
    });

    if ("redirect" in serverSideProps || "error" in serverSideProps.props) {
      throw new Error();
    }

    const { getByRole } = testRender(
      <AppProvider initialState={getMockAppState({ localeCode })}>
        <HomePage {...serverSideProps.props} />
      </AppProvider>,
    );

    await act(async () => {
      expect(
        getByRole("heading", {
          name: sharedStrings.siteTitle,
        }),
      ).toBeInTheDocument();
    });
  });
});
