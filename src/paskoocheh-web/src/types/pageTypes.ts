import type {
  GetServerSidePropsContext,
  NextPage,
  PreviewData,
  Redirect,
} from "next";
import type { ParsedUrlQuery } from "querystring";

import type { ErrorPageContentProps } from "src/components/ErrorPageContent";
import type { GqlPlatform } from "src/generated/graphQl";

export type PaskoochehPageRequiredProps = {
  platforms: Array<GqlPlatform> | null;
};

/* eslint-disable @typescript-eslint/member-ordering, @typescript-eslint/array-type, @typescript-eslint/no-explicit-any */

/**
 * Context object passed into `getServerSideProps`.
 * @link https://nextjs.org/docs/api-reference/data-fetching/get-server-side-props#context-parameter
 *
 * @remarks ASL19  modifications:
 *
 * - `Params` type argument is required, and `params` key is always set (not
 *   optional like in GetServerSidePropsContext)
 *
 * @see `GetServerSidePropsContext` in [`next` types](../../node_modules/next/types/index.d.ts)
 */
type PaskoochehGetServerSidePropsContext<
  Params extends ParsedUrlQuery,
  Preview extends PreviewData = PreviewData,
> = GetServerSidePropsContext<Params, Preview> & {
  params: Params;
};

/**
 * Server-side Rendering feature for Next.js.
 * @link https://nextjs.org/docs/basic-features/data-fetching/get-server-side-props
 * @link https://nextjs.org/docs/basic-features/typescript#static-generation-and-server-side-rendering
 * @example
 * ```ts
 * export const getServerSideProps: GetServerSideProps = async (context) => {
 *  // ...
 * }
 *
 * @remarks ASL19 modifications:
 *
 * - Can return `{ props: { error: ErrorPageContentProps } }`, which causes _app
 *   to render an error page
 *
 * - Don’t use Next’s `GetServerSidePropsResult`, which allows returning `{
 *   notFound: true }` (we handle this use case via `ErrorPageContentProps`) or
 *   `{ props: Promise<Props> }` (which we don’t use, and breaks Jest tests)
 *
 * @see `GetServerSideProps` in [`next` types](../../node_modules/next/types/index.d.ts)
 */
export type PaskoochehGetServerSideProps<
  Props extends PaskoochehPageRequiredProps = PaskoochehPageRequiredProps,
  Params extends ParsedUrlQuery = {},
  Preview extends PreviewData = PreviewData,
> = (
  context: PaskoochehGetServerSidePropsContext<Params, Preview>,
) => Promise<
  { props: Props | { error: ErrorPageContentProps } } | { redirect: Redirect }
>;

export type PaskoochehNextPage<
  Props extends PaskoochehPageRequiredProps = PaskoochehPageRequiredProps,
> = NextPage<Props>;

/* eslint-enable @typescript-eslint/member-ordering, @typescript-eslint/array-type, @typescript-eslint/no-explicit-any */
