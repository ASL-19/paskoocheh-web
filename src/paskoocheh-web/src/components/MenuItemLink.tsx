import { MenuItem } from "@ariakit/react/menu";
import { StylableFC } from "@asl-19/react-dom-utils";
import { EmotionJSX } from "@emotion/react/types/jsx-namespace";
import Link from "next/link";
import { memo, useMemo } from "react";

const MenuItemLink: StylableFC<{
  content: EmotionJSX.Element | string;
  href: string;
}> = memo(({ content, href, ...remainingProps }) => {
  const link = useMemo(
    () => <Link href={href}>{content}</Link>,
    [content, href],
  );

  return <MenuItem render={link} {...remainingProps} />;
});

MenuItemLink.displayName = "MenuItemLink";

export default MenuItemLink;
