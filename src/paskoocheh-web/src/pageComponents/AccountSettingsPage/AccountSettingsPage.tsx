import { useCallback } from "react";

import useDashboardPageAccessAndLoadingLogic, {
  FetchPropsOrErrorMessage,
} from "src/hooks/useDashboardPageAccessAndLoading";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import AccountSettingsPageContent, {
  AccountSettingsPageContentProps,
} from "src/pageComponents/AccountSettingsPage/AccountSettingsPageContent";
import { useAppStrings } from "src/stores/appStore";
import { PaskoochehNextPage } from "src/types/pageTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

// =============
// === Types ===
// =============

const AccountSettingsPage: PaskoochehNextPage = () => {
  const strings = useAppStrings();
  const queryPlatform = useQueryOrDefaultPlatformSlug();

  const fetchPropsOrErrorMessage: FetchPropsOrErrorMessage<AccountSettingsPageContentProps> =
    useCallback(async () => {
      const graphQlSdk = await getGraphQlSdk();

      try {
        const [userResponse] = await Promise.all([graphQlSdk.getMe()]);

        const user = userResponse.me;

        if (!user)
          return {
            errorMessage: strings.shared.dashboard.errorMessages.default,
          };

        return {
          props: {
            platforms: queryPlatform,
            user,
          },
        };
      } catch {
        return {
          errorMessage: strings.shared.dashboard.errorMessages.default,
        };
      }
    }, [queryPlatform, strings.shared.dashboard.errorMessages.default]);

  return useDashboardPageAccessAndLoadingLogic<AccountSettingsPageContentProps>(
    {
      fetchPropsOrErrorMessage,
      PageContentComponent: AccountSettingsPageContent,
    },
  );
};

export default AccountSettingsPage;
