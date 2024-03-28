import { useCallback, useEffect, useRef } from "react";

import { useAppDispatch } from "src/stores/appStore";
import getRefreshToken from "src/utils/api/getRefreshToken";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";

/**
 * On first render verify the localStorage token and dispatch it to appStore if
 * it’s valid.
 */
const useVerifyAndDispatchLocalStorageTokenOnFirstRender = () => {
  const appDispatch = useAppDispatch();

  const hasRun = useRef(false);

  const verifyAndDispatchToken = useCallback(async () => {
    const refreshToken = getRefreshToken();

    if (refreshToken) {
      try {
        const graphQlSdk = await getGraphQlSdk({ method: "POST" });

        if (!graphQlSdk.hasAccessToken) {
          appDispatch({ type: "usernameChanged", username: null });
          return;
        }

        const meResponse = await graphQlSdk.getMe();

        if (meResponse.me?.username) {
          appDispatch({
            type: "usernameChanged",
            username: meResponse.me.username,
          });

          return;
        }
      } catch (error) {
        console.error("Error while verifying account:", error);
      }
    }

    appDispatch({ type: "usernameChanged", username: null });
  }, [appDispatch]);

  useEffect(() => {
    if (!hasRun.current) {
      hasRun.current = true;
      verifyAndDispatchToken();
    }
  }, [verifyAndDispatchToken]);
};

export default useVerifyAndDispatchLocalStorageTokenOnFirstRender;
