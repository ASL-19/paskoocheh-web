import { match } from "ts-pattern";

import type {
  getSdk,
  GqlDoTokenAuth,
  GqlDoTokenAuthVariables,
} from "src/generated/graphQl";
import usersByUsername from "src/test/data/usersByUsername";

const doTokenAuth: ReturnType<typeof getSdk>["doTokenAuth"] = (variables) =>
  match<GqlDoTokenAuthVariables, Promise<GqlDoTokenAuth>>(variables)
    .with(
      {
        password: usersByUsername.mockuser.username,
        username: usersByUsername.mockuser.username,
      },
      () =>
        Promise.resolve({
          tokenAuth: {
            errors: null,
            refreshToken: { token: usersByUsername.mockuser.username },
            success: true,
            user: usersByUsername.mockuser,
          },
        }),
    )
    .otherwise(() =>
      Promise.resolve({
        tokenAuth: {
          errors: {
            nonFieldErrors: [
              {
                code: "invalid_credentials",
                message: "Please, enter valid credentials.",
              },
            ],
          },
          refreshToken: null,
          success: false,
          user: null,
        },
      }),
    );

export default doTokenAuth;
