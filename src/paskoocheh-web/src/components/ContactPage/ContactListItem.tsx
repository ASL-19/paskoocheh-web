import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ButtonLink from "src/components/ButtonLink";
import StaticImage from "src/components/StaticImage";
import { ContactAppInfo } from "src/pageComponents/ContactPage/ContactPage";
import { paragraphP1Regular, paragraphP3SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(
  {
    alignItems: "center",
    backgroundColor: colors.primary50,
    borderRadius: "0.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    padding: "2rem",
    width: "27.8125rem",
  },
  breakpointStyles({
    singleColumn: {
      lt: {
        width: "100%",
      },
    },
  }),
);

const logo = css({
  height: "3.125rem",
  width: "3.125rem",
});

const textContainer = css({
  alignItems: "center",
  display: "flex",
  flexDirection: "column",
  gap: "0.25rem",
});

const name = css(paragraphP3SemiBold);

const description = css(paragraphP1Regular, { color: colors.secondary400 });

const link = css({
  // padding: "0 2rem",
  width: "12.25rem",
});

const ContactListItem: StylableFC<{ contact: ContactAppInfo }> = memo(
  ({ className, contact }) => (
    <div className={className} css={container}>
      <StaticImage
        css={logo}
        staticImageData={contact.logo}
        alt={contact.name}
      />

      <div css={textContainer}>
        <h2 css={name}>{contact.name}</h2>
        <p css={description}>{contact.description}</p>
      </div>

      <ButtonLink
        variant="primary"
        text={contact.urlLabel}
        href={contact.url}
        css={link}
      />
    </div>
  ),
);

ContactListItem.displayName = "ContactListItem";

export default ContactListItem;
