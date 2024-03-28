import { apiQueryItemLimit } from "src/values/apiValues";

const getLimitedItemCount = ({ count }: { count: number }) =>
  count > apiQueryItemLimit ? apiQueryItemLimit : count;

export default getLimitedItemCount;
