import { css } from "@emotion/react";
import { FC, memo } from "react";
import { FallbackProps } from "react-error-boundary";

import Layout from "src/components/Layout/Layout";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP3Regular } from "src/styles/typeStyles";

// =============
// === Types ===
// =============

export type ClientSideErrorFallbackStrings = {
  description: string;
  title: string;
};

const container = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  maxWidth: "40rem",
  paddingBottom: "6rem",
  paddingTop: "3rem",
});

const heading = css({
  fontSize: "2rem",
  textAlign: "center",
});

const ClientSideErrorFallback: FC<FallbackProps> = memo(({ error }) => {
  const strings = useAppStrings();

  const description = strings.ClientSideErrorFallback.description;

  const titleLocalized = strings.ClientSideErrorFallback.title;

  return (
    <Layout platforms={null}>
      <PageContainer>
        <PageSegment centeredContainerCss={container}>
          <PageMeta
            canonicalPath={null}
            description={description}
            image={null}
            isAvailableInAlternateLocales={false}
            title={titleLocalized}
          />
          <h1 css={heading} id="main-heading">
            {titleLocalized}
          </h1>

          <p css={paragraphP3Regular}>{description}</p>

          <pre dir="ltr">{error.stack}</pre>
        </PageSegment>
      </PageContainer>
    </Layout>
  );
});
ClientSideErrorFallback.displayName = "ClientSideErrorFallback";

export default ClientSideErrorFallback;
