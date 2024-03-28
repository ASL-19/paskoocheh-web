import { useAppLocaleInfo } from "src/stores/appStore";
import formatNumber from "src/utils/formatNumber";

/**
 * Same as formatNumber, but gets and injects localeCode argument from appStore.
 */
const useFormattedNumber = (
  args: Omit<Parameters<typeof formatNumber>[0], "localeCode">,
) => {
  const { localeCode } = useAppLocaleInfo();

  return formatNumber({ ...args, localeCode });
};

export default useFormattedNumber;
