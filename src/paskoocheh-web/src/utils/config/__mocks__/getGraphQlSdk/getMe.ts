import type { getSdk } from "src/generated/graphQl";
import minimalUsersByUsername from "src/test/data/minimalUsersByUsername";
import getRefreshToken from "src/utils/api/getRefreshToken";

const getMe: ReturnType<typeof getSdk>["getMe"] = () =>
  Promise.resolve({
    me: minimalUsersByUsername[getRefreshToken() ?? ""] ?? null,
  });

export default getMe;
