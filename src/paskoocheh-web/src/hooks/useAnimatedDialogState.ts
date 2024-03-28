import {
  DialogStore,
  DialogStoreProps,
  useDialogStore,
} from "@ariakit/react/dialog";

export type AnimatedDialogStore = DialogStore & {
  animated: true;
};

/**
 * Wrapper for Ariakit’s `useDialogState` hook that sets the `animated` argument
 * to true and tightens the returned `DisclosureState` for use in `AuthOverlay`
 * and `AnimatedOverlay`.
 *
 * This is important because `AuthOverlay` dialogs will fail to open if the
 * passed dialogState doesn’t have `{animated: true}`.
 */
const useAnimatedDialogStore = (args?: Omit<DialogStoreProps, "animated">) =>
  useDialogStore({ ...args, animated: true }) as AnimatedDialogStore;

export default useAnimatedDialogStore;
