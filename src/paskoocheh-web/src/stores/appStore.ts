import constate from "constate";
import { useReducer } from "react";
import { match } from "ts-pattern";

import { GqlPlatform } from "src/generated/graphQl";
import { Strings } from "src/types/stringTypes";
import reducerLog from "src/utils/store/reducerLog";
import { LocaleCode } from "src/values/localeValues";

// =============
// === Types ===
// =============

export type AppLocaleInfo = {
  dateTimeFormatter: Intl.DateTimeFormat;
  direction: "ltr" | "rtl";
  localeCode: LocaleCode;
  numberFormatter: Intl.NumberFormat;
};

export type AppRouteChangeInfo = {
  routeChangeIsInProgress: boolean;
  routeChangeTimestamp: number;
};

export type AppState = {
  localeInfo: AppLocaleInfo;
  platforms: Array<GqlPlatform> | null;
  routeChangeInfo: AppRouteChangeInfo;
  strings: Strings;
  username: string | null | undefined;
};

/* eslint-disable @typescript-eslint/member-ordering */
type AppAction =
  | { type: "platformsLoaded"; platforms: Array<GqlPlatform> }
  | { type: "routeChangeCompleted" }
  | { type: "routeChangeStarted" }
  | { type: "usernameChanged"; username: string | null };
/* eslint-enable @typescript-eslint/member-ordering */

// ===============
// === Reducer ===
// ===============

const appReducer = (state: AppState, action: AppAction) => {
  const newState: AppState = match(action)
    .with({ type: "platformsLoaded" }, (action) => ({
      ...state,
      platforms: action.platforms,
    }))
    .with({ type: "routeChangeCompleted" }, () => ({
      ...state,
      routeChangeInfo: {
        ...state.routeChangeInfo,
        routeChangeIsInProgress: false,
      },
    }))
    .with({ type: "routeChangeStarted" }, () => ({
      ...state,
      routeChangeInfo: {
        routeChangeIsInProgress: true,
        routeChangeTimestamp: Date.now(),
      },
    }))
    .with({ type: "usernameChanged" }, (action) => ({
      ...state,
      username: action.username,
    }))
    .exhaustive();

  reducerLog({
    action,
    newState,
    state,
    storeName: "app",
  });

  return newState;
};

const useApp = ({ initialState }: { initialState: AppState }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return { dispatch, state };
};

export const [
  AppProvider,
  useAppDispatch,
  useAppLocaleInfo,
  useAppPlatforms,
  useAppRouteChangeInfo,
  useAppStrings,
  useAppUsername,
] = constate(
  useApp,
  (value) => value.dispatch,
  (value) => value.state.localeInfo,
  (value) => value.state.platforms,
  (value) => value.state.routeChangeInfo,
  (value) => value.state.strings,
  (value) => value.state.username,
);
