import { GraphQLClient } from "graphql-request";

import { getSdk } from "src/generated/graphQl";
import { SdkWithHasAccessToken } from "src/types/apiTypes";
import getRefreshToken from "src/utils/api/getRefreshToken";
import removeRefreshToken from "src/utils/api/removeRefreshToken";
import setRefreshToken from "src/utils/api/setRefreshToken";
import { timeoutApi } from "src/values/apiValues";

type GraphQlRequestMethod = "GET" | "POST";

const getClient = ({
  method,
  signal,
}: {
  method: GraphQlRequestMethod;
  signal?: AbortSignal;
}) =>
  new GraphQLClient(`${process.env.NEXT_PUBLIC_BACKEND_URL}/graphql/`, {
    fetch,
    jsonSerializer: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
    method,
    signal,
  });

/**
 * Get a unique instance of GraphQL that will abort its request after the
 * specified timeout (defaults to timeout).
 *
 * Supports passing a custom abortController, which is useful if you need the
 * ability to abort the request earlier.
 *
 * @param abortController - Instance of AbortController. Can cancel request from
 * outside with abortController.abort().
 *
 * @param timeout - Timeout before abort in ms.
 */
const getGraphQlSdk = async ({
  abortController = new AbortController(),
  method = "GET",
  timeout = timeoutApi,
}: {
  abortController?: AbortController;
  method?: GraphQlRequestMethod;
  timeout?: number;
} = {}): Promise<SdkWithHasAccessToken> => {
  setTimeout(() => {
    abortController.abort();
  }, timeout);

  const client = getClient({ method, signal: abortController?.signal });

  // On server this will always be null; on client this will be string if
  // localStorage refreshToken is set.
  const oldRefreshToken = getRefreshToken();

  const { accessToken, newRefreshToken } = oldRefreshToken
    ? await (async () => {
        const refreshTokenSdk = getSdk(getClient({ method: "POST" }));

        try {
          const refreshTokenResponse = await refreshTokenSdk.doRefreshToken({
            refreshToken: oldRefreshToken,
          });

          return {
            accessToken: refreshTokenResponse.refreshToken.token?.token ?? null,
            newRefreshToken:
              refreshTokenResponse.refreshToken.refreshToken?.token ?? null,
          };
        } catch {
          return {
            accessToken: null,
            newRefreshToken: null,
          };
        }
      })()
    : {
        accessToken: null,
        newRefreshToken: null,
      };

  if (newRefreshToken) {
    setRefreshToken(newRefreshToken);
  } else {
    removeRefreshToken();
  }

  const graphQlSdk = getSdk(client, async (action) => {
    const requestHeaders = accessToken
      ? {
          Authorization: `JWT ${accessToken}`,
        }
      : undefined;

    const result = await action(requestHeaders);

    return result;
  });

  const graphQlSdkWithHasAccessToken = {
    ...graphQlSdk,
    hasAccessToken: !!accessToken,
  };

  return Promise.resolve(graphQlSdkWithHasAccessToken);
};

export default getGraphQlSdk;
