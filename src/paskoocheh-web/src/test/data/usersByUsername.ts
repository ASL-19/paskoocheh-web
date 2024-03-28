import { asType } from "@asl-19/js-utils";

import { GqlUser } from "src/generated/graphQl";

// Note: At a later date the properties of GqlUser might be different than
// GqlMinimalUser
const usersByUsername = {
  mockuser: asType<GqlUser>({
    email: "mockuser@paskoocheh.com",
    firstName: "Mock",
    id: "1",
    lastName: "User",
    username: "mockuser",
  }),
};

export default usersByUsername;
