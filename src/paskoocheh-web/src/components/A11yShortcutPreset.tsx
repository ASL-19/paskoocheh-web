import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import A11yShortcut from "src/components/A11yShortcut";
import { useAppStrings } from "src/stores/appStore";

export type A11yShortcutPresetStrings = {
  skipToNavigation: string;
};

const A11yShortcutPreset: StylableFC<{
  preset: "skipToNavigation";
}> = memo(({ className, preset }) => {
  const strings = useAppStrings().A11yShortcutPreset;

  const { targetId, text } = (() => {
    if (preset === "skipToNavigation") {
      return {
        targetId: "nav-heading",
        text: strings.skipToNavigation,
      };
    }

    console.error("A11yShortcutPreset was passed unexpected preset property!");

    return {
      targetId: "",
      text: "",
    };
  })();

  return <A11yShortcut className={className} targetId={targetId} text={text} />;
});

A11yShortcutPreset.displayName = "A11yShortcutPreset";

export default A11yShortcutPreset;
