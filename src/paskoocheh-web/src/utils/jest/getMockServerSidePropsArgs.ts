import { IncomingMessage, ServerResponse } from "http";
import { GetServerSidePropsContext } from "next";
import { createRequest, createResponse } from "node-mocks-http";

const getMockServerSidePropsArgs: () => Omit<
  GetServerSidePropsContext<{}, {}>,
  "query"
> = () => {
  const req = createRequest<IncomingMessage & { cookies: {} }>();
  const res = createResponse<ServerResponse>();

  return {
    req,
    res,
    resolvedUrl: "",
  };
};

export default getMockServerSidePropsArgs;
