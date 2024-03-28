import { useRouter } from "next/router";
import {
  Dispatch,
  MouseEventHandler,
  SetStateAction,
  useCallback,
} from "react";

import { AppNavLinkInfo } from "src/components/App/AppTabContent/AppNavLinkListItem";
import useFocusElementAfterRender from "src/hooks/useFocusElementAfterRender";

const useOnSectionLinkClick = ({
  linkInfo,
  setActiveSectionId,
}: {
  linkInfo: AppNavLinkInfo;
  setActiveSectionId: Dispatch<SetStateAction<string>>;
}) => {
  const router = useRouter();

  const focusElementAfterRender = useFocusElementAfterRender();

  const onClick: MouseEventHandler = useCallback(
    (event) => {
      event.preventDefault();

      const pathWithoutHash = router.asPath.split("#")[0] as string;

      router.replace(pathWithoutHash, undefined, {
        scroll: false,
        shallow: true,
      });

      setActiveSectionId(linkInfo.id);

      if (linkInfo.navItemRef.current) {
        // Scroll into view horizontally (will scroll vertically if it’s
        // clicked while entirely out of view, which would only ever happen
        // with screen readers/keyboard navigation)
        linkInfo.navItemRef.current.scrollIntoView({
          block: "nearest",
          inline: "nearest",
        });
      }

      if (linkInfo.sectionRef.current) {
        focusElementAfterRender(linkInfo.sectionRef.current);
      }
    },
    [focusElementAfterRender, linkInfo, router, setActiveSectionId],
  );

  return onClick;
};

export default useOnSectionLinkClick;
