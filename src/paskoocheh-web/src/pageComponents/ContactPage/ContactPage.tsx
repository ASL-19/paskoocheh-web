import { css } from "@emotion/react";
import { StaticImageData } from "next/image";

import A11yShortcutPreset from "src/components/A11yShortcutPreset";
import ContactListItem from "src/components/ContactPage/ContactListItem";
import PageContainer from "src/components/Page/PageContainer";
import PageMeta from "src/components/Page/PageMeta";
import PageSegment from "src/components/Page/PageSegment";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import gmailLogo from "src/static/contact/gmailLogo.png";
import telegramLogo from "src/static/contact/telegramLogo.png";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";
import { headingH3SemiBold, headingH5SemiBold } from "src/styles/typeStyles";
import {
  PaskoochehNextPage,
  PaskoochehPageRequiredProps,
} from "src/types/pageTypes";
import { breakpointStyles } from "src/utils/media/media";
// =============
// === Types ===
// =============

export type ContactPageProps = PaskoochehPageRequiredProps & {
  toolPk: number | null;
};

export type ContactPageStrings = {
  /**
   * Text for contacts box
   */
  contacts: {
    email: {
      description: string;
      name: string;
      urlLabel: string;
    };
    telegram: {
      description: string;
      name: string;
      urlLabel: string;
    };
  };
  /**
   * Page SEO description.
   */
  pageDescription: string;

  /**
   * Title (used for heading and page title).
   */
  title: string;
};

export type ContactAppInfo = {
  description: string;
  logo: StaticImageData;
  name: string;
  url: string;
  urlLabel: string;
};

// ==============
// === Styles ===
// ==============
const container = css(
  {
    display: "flex",
    flexDirection: "column",
    gap: "3.25rem",
    padding: "3.25rem 1rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        gap: "1rem",
      },
    },
  }),
);
const heading = css(
  headingH3SemiBold,
  breakpointStyles({
    singleColumn: {
      lt: headingH5SemiBold,
    },
  }),
);
const contactContainer = css(
  {
    display: "flex",
    gap: "1.25rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        flexDirection: "column",
      },
    },
  }),
);
// ==============================
// === Next.js page component ===
// ==============================

const ContactPage: PaskoochehNextPage<ContactPageProps> = ({ toolPk }) => {
  const { localeCode } = useAppLocaleInfo();
  const { ContactPage: strings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  const contactInfos: Array<ContactAppInfo> = [
    {
      description: strings.contacts.telegram.description,
      logo: telegramLogo,
      name: strings.contacts.telegram.name,
      url: "",
      urlLabel: strings.contacts.telegram.urlLabel,
    },
    {
      description: strings.contacts.email.description,
      logo: gmailLogo,
      name: strings.contacts.email.name,
      url: routeUrls.writeYourMessage({
        localeCode,
        platform: queryOrDefaultPlatformSlug,
        // TODO: Change to toolSlug once #559 is done
        tool: toolPk,
      }),
      urlLabel: strings.contacts.email.urlLabel,
    },
  ];
  return (
    <PageContainer>
      <PageMeta
        canonicalPath={routeUrls.contact({
          localeCode,
          platform: queryOrDefaultPlatformSlug,
          tool: toolPk,
        })}
        description={strings.pageDescription}
        image={null}
        isAvailableInAlternateLocales={true}
        title={strings.title}
      />
      <PageSegment centeredContainerCss={container}>
        <h1 css={heading} id="main-heading">
          {strings.title}
        </h1>
        <div css={contactContainer}>
          {contactInfos.map((contact) => (
            <ContactListItem contact={contact} key={contact.name} />
          ))}
        </div>
      </PageSegment>

      <A11yShortcutPreset preset="skipToNavigation" />
    </PageContainer>
  );
};

export default ContactPage;
