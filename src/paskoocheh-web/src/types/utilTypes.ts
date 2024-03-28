/* eslint-disable @typescript-eslint/no-explicit-any */

// Via https://stackoverflow.com/a/60437613
export type Replacement<M extends [any, any], T> = M extends any
  ? [T] extends [M[0]]
    ? M[1]
    : never
  : never;

// Via https://stackoverflow.com/a/60437613
export type DeepReplace<T, M extends [any, any]> = {
  [P in keyof T]: T[P] extends M[0]
    ? Replacement<M, T[P]>
    : T[P] extends object
      ? DeepReplace<T[P], M>
      : T[P];
};

/**
 * Create a type that removes nullish (optional, undefined and null) types from
 * the given keys. The remaining keys are kept as is.
 *
 * @see https://lorefnon.tech/2020/02/02/conditionally-making-optional-properties-mandatory-in-typescript/
 * @see https://github.com/sindresorhus/type-fest/pull/245
 */
export type SetNonNullable<T extends {}, K extends keyof T> = {
  [TK in keyof T]: TK extends K ? NonNullable<T[TK]> : T[TK];
};
