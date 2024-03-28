import { apiQueryItemLimit } from "src/values/apiValues";

const getLimitedHasNextPage = ({
  count,
  hasNextPage,
}: {
  count: number;
  hasNextPage: boolean;
}) => count < apiQueryItemLimit && hasNextPage;

export default getLimitedHasNextPage;
