import { FC, useEffect, useState } from "react";

import AccessDenied from "src/components/UserAccess/AccessDenied";
import AccessErrorMessage from "src/components/UserAccess/AccessErrorMessage";
import AccessLoadingIndicator from "src/components/UserAccess/AccessLoadingIndicator";
import { AppState, useAppUsername } from "src/stores/appStore";

type PropsOrErrorMessage<Props> =
  | { props: Props }
  | { errorMessage: string }
  | null;

export type FetchPropsOrErrorMessage<Props> = ({
  username,
}: {
  username: NonNullable<AppState["username"]>;
}) => Promise<PropsOrErrorMessage<Props>>;

const useDashboardPageAccessAndLoadingLogic = <Props,>({
  PageContentComponent,
  fetchPropsOrErrorMessage,
}: {
  PageContentComponent: FC<Props>;
  fetchPropsOrErrorMessage: FetchPropsOrErrorMessage<Props>;
}) => {
  const username = useAppUsername();

  const [pageContentProps, setPageContentProps] =
    useState<PropsOrErrorMessage<Props> | null>(null);

  useEffect(() => {
    if (typeof username === "undefined") {
      return;
    }

    (async () => {
      const props = username
        ? await fetchPropsOrErrorMessage({ username })
        : null;

      setPageContentProps(props);
    })();
  }, [fetchPropsOrErrorMessage, username]);

  if (username === null) {
    return <AccessDenied />;
  }

  if (typeof username === "undefined" || pageContentProps === null) {
    return <AccessLoadingIndicator />;
  }

  if ("errorMessage" in pageContentProps) {
    return <AccessErrorMessage errorMessage={pageContentProps.errorMessage} />;
  }
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  return <PageContentComponent {...pageContentProps.props!} />;
};

export default useDashboardPageAccessAndLoadingLogic;
