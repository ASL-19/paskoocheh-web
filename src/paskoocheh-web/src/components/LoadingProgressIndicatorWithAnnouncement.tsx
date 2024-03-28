import { announce } from "@asl-19/js-dom-utils";
import LoadingProgressIndicator, {
  LoadingProgressIndicatorProps,
} from "@asl-19/react-loading-progress-indicator";
import { FC, memo, useEffect } from "react";

/**
 * This renders the loading indicator and announces its label when it appears.
 *
 * This functionality will eventually be integrated into
 * LoadingProgressIndicator so we won’t need a custom wrapper component.
 */
const LoadingProgressIndicatorWithAnnouncement: FC<LoadingProgressIndicatorProps> =
  memo((props) => {
    useEffect(() => {
      const announceLoadingTimeoutId = setTimeout(() => {
        if (props.isLoading) {
          announce({
            priority: "assertive",
            text: props.label,
          });
        }
      }, 300);

      return () => {
        clearTimeout(announceLoadingTimeoutId);
      };
    }, [props.isLoading, props.label]);

    return <LoadingProgressIndicator {...props} />;
  });

LoadingProgressIndicatorWithAnnouncement.displayName =
  "LoadingProgressIndicatorWithAnnouncement";

export default LoadingProgressIndicatorWithAnnouncement;
