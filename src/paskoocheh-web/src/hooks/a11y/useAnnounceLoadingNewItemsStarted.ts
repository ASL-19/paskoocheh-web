import { announce } from "@asl-19/js-dom-utils";
import { useCallback } from "react";

import { useAppStrings } from "src/stores/appStore";

const useAnnounceLoadingNewItemsStarted = () => {
  const { shared: sharedStrings } = useAppStrings();

  return useCallback(() => {
    announce({
      priority: "assertive",
      text: sharedStrings.a11yAnnouncements.loadingNewItemsStarted,
    });
  }, [sharedStrings.a11yAnnouncements.loadingNewItemsStarted]);
};

export default useAnnounceLoadingNewItemsStarted;
