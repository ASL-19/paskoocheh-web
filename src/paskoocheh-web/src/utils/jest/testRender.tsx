import { render as defaultRender } from "@testing-library/react";
import { RouterContext } from "next/dist/shared/lib/router-context.shared-runtime";
import { NextRouter } from "next/router";

export * from "@testing-library/react";

// --------------------------------------------------
// Override the default test render with our own
//
// You can override the router mock like this:
//
// const { baseElement } = render(<MyComponent />, {
//   router: { pathname: '/my-custom-pathname' },
// });
// --------------------------------------------------
type DefaultParams = Parameters<typeof defaultRender>;
type RenderUI = DefaultParams[0];
type RenderOptions = DefaultParams[1] & { router?: Partial<NextRouter> };

const mockRouter: NextRouter = {
  asPath: "/",
  back: jest.fn(),
  basePath: "",
  beforePopState: jest.fn(),
  events: {
    emit: jest.fn(),
    off: jest.fn(),
    on: jest.fn(),
  },
  forward: jest.fn(),
  isFallback: false,
  isLocaleDomain: false,
  isPreview: false,
  isReady: true,
  pathname: "/",
  prefetch: jest.fn(),
  push: jest.fn(),
  query: {},
  reload: jest.fn(),
  replace: jest.fn(),
  route: "/",
};

const testRender = (
  ui: RenderUI,
  { router, wrapper, ...options }: RenderOptions = {},
) => {
  if (!wrapper) {
    // eslint-disable-next-line no-param-reassign, react/display-name
    wrapper = ({ children }) => (
      <RouterContext.Provider value={{ ...mockRouter, ...router }}>
        {children}
      </RouterContext.Provider>
    );
  }

  return defaultRender(ui, { wrapper, ...options });
};

export default testRender;
