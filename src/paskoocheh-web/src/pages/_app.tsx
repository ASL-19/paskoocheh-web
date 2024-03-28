import { NextComponentType } from "next";
import { AppProps } from "next/app";
import dynamic from "next/dynamic";
import { FC, StrictMode, Suspense, useMemo } from "react";
import { ErrorBoundary } from "react-error-boundary";

import ErrorPageContent, {
  ErrorPageContentProps,
} from "src/components/ErrorPageContent";
import Layout from "src/components/Layout/Layout";
import LoadingProgressIndicatorWithAnnouncement from "src/components/LoadingProgressIndicatorWithAnnouncement";
import useAddHydratedClassName from "src/hooks/app/useAddHydratedClassName";
import useDispatchAppRouteChangeActions from "src/hooks/app/useDispatchAppRouteChangeActions";
import useDynamicFocusOutlines from "src/hooks/app/useDynamicFocusOutlines";
import useFocusMainHeadingOnRouteChange from "src/hooks/app/useFocusMainHeadingOnRouteChange";
import useGoogleTagRouteChangePageViewTracking from "src/hooks/app/useGoogleTagRouteChangePageViewTracking";
import useSetQueryPlatformIfMissingOrInvalid from "src/hooks/app/useSetQueryPlatformIfMissingOrInvalid";
import useVerifyAndDispatchLocalStorageTokenOnFirstRender from "src/hooks/app/useVerifyAndDispatchTokenOnFirstRender";
import {
  AppLocaleInfo,
  AppProvider,
  AppState,
  useAppLocaleInfo,
  useAppRouteChangeInfo,
} from "src/stores/appStore";
import { PaskoochehPageRequiredProps } from "src/types/pageTypes";
import { Strings } from "src/types/stringTypes";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import { MediaContextProvider } from "src/utils/media/media";
import colors from "src/values/colors";

const ClientSideErrorFallback = dynamic(
  () => import("src/components/ClientSideErrorFallback"),
);

type PaskoochehAppProps = AppProps<
  PaskoochehPageRequiredProps & {
    // Returned by src/utils/getServerSideProps/errorProps
    error?: ErrorPageContentProps;
    strings?: Strings;
  }
>;

const PaskoochehApp: FC<PaskoochehAppProps> = ({ Component, pageProps }) => {
  const { direction, localeCode } = useAppLocaleInfo();
  const routeChangeInfo = useAppRouteChangeInfo();

  useAddHydratedClassName();
  useDispatchAppRouteChangeActions();
  useDynamicFocusOutlines();
  useFocusMainHeadingOnRouteChange();
  useSetQueryPlatformIfMissingOrInvalid();
  useGoogleTagRouteChangePageViewTracking({ isActive: true });
  useVerifyAndDispatchLocalStorageTokenOnFirstRender();

  if (pageProps.error) {
    return (
      <Layout platforms={pageProps.platforms}>
        <ErrorPageContent {...pageProps.error} />
      </Layout>
    );
  }

  return (
    <Layout platforms={pageProps.platforms}>
      {routeChangeInfo.routeChangeTimestamp > 0 && (
        <LoadingProgressIndicatorWithAnnouncement
          color={colors.blue}
          direction={direction}
          isLoading={routeChangeInfo.routeChangeIsInProgress}
          // label strings are hard-coded since we don’t want to import
          // stringsEn and stringsFa from this file. If we then every English
          // and Persian string would be loaded for all pages
          /* cSpell:disable-next-line  */
          label={localeCode === "en" ? "Loading" : "در حال بارگذاری"}
          key={routeChangeInfo.routeChangeTimestamp}
          // shouldBeVisibleBeforeFirstTick
        />
      )}
      <Component {...pageProps} />
    </Layout>
  );
};

const EgAppWrapper: FC<PaskoochehAppProps> = (props) => {
  const { Component, pageProps, router } = props;

  // ----------------
  // --- appStore ---
  // ----------------
  const { dateTimeFormatter, direction, localeCode, numberFormatter } =
    getLocaleMetadata(router.asPath.slice(1, 3));

  const localeInfo: AppLocaleInfo = useMemo(
    () => ({
      dateTimeFormatter,
      direction,
      localeCode,
      numberFormatter,
    }),
    [dateTimeFormatter, direction, localeCode, numberFormatter],
  );

  const strings = ((Component as NextComponentType & { strings?: Strings })
    .strings || pageProps.strings) as Strings;

  const appStoreInitialState: AppState = useMemo(
    () => ({
      localeInfo,
      platforms: pageProps.platforms,
      routeChangeInfo: {
        routeChangeIsInProgress: false,
        routeChangeTimestamp: 0,
      },
      strings,
      username: undefined,
    }),
    [localeInfo, pageProps.platforms, strings],
  );

  const errorBoundaryResetKeys = useMemo(
    () => [router.asPath],
    [router.asPath],
  );

  return (
    <StrictMode>
      <AppProvider initialState={appStoreInitialState}>
        <MediaContextProvider>
          <Suspense>
            <ErrorBoundary
              FallbackComponent={ClientSideErrorFallback}
              resetKeys={errorBoundaryResetKeys}
            >
              <PaskoochehApp {...props} />
            </ErrorBoundary>
          </Suspense>
        </MediaContextProvider>
      </AppProvider>
    </StrictMode>
  );
};

export default EgAppWrapper;
