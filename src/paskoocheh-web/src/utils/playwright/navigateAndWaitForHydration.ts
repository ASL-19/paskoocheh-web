import { Page } from "@playwright/test";

/**
 * Navigate to the specified path and wait for Next.js to hydrate, returning
 * `page.goto` response.
 *
 * Without this there can be race conditions if e.g. we navigate to a page then
 * immediately click a button with an event handler we expect to run. At this
 * point the Next.js hydration may not be complete yet, in which case nothing
 * would happen when the button is clicked.
 *
 * This case can technically happen for users as well, but it’s much less likely
 * since they have human reflexes, and it’s not obvious how we could address
 * this.
 */
const navigateAndWaitForHydration = async ({
  page,
  path,
  username,
}: {
  page: Page;
  path: string;
  username?: string;
}) => {
  const response = await page.goto(path);

  if (username) {
    // Via https://github.com/microsoft/playwright/issues/6258#issuecomment-1723382085
    const innerLocalStorage = await page.evaluateHandle(
      () => window.localStorage,
    );

    await innerLocalStorage.evaluate(
      (storage, username) => storage.setItem("refreshToken", username),
      username,
    );

    // Reload page so localStorage refreshToken is read by
    // useVerifyAndDispatchLocalStorageTokenOnFirstRender
    await page.reload();
  }

  await page.locator("html.hydrated").waitFor();

  return response;
};

export default navigateAndWaitForHydration;
