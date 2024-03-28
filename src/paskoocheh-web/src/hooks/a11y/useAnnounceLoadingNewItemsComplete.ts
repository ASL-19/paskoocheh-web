import { announce } from "@asl-19/js-dom-utils";
import { useCallback } from "react";

import { useAppStrings } from "src/stores/appStore";

const useAnnounceLoadingNewItemsComplete = () => {
  const { shared: sharedStrings } = useAppStrings();

  return useCallback(
    ({ count }: { count: number }) => {
      announce({
        priority: "assertive",
        text: sharedStrings.a11yAnnouncements.loadingNewItemsComplete.replace(
          "{count}",
          count.toString(),
        ),
      });
    },
    [sharedStrings.a11yAnnouncements.loadingNewItemsComplete],
  );
};

export default useAnnounceLoadingNewItemsComplete;
