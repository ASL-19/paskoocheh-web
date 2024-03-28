import { useRouter } from "next/router";
import { FormEventHandler, RefObject, useCallback } from "react";
import { match, P } from "ts-pattern";

import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppPlatforms } from "src/stores/appStore";

const useSearchFormOnSubmit = ({
  formElementRef,
}: {
  formElementRef: RefObject<HTMLFormElement>;
}) => {
  const router = useRouter();
  const { localeCode } = useAppLocaleInfo();
  const platforms = useAppPlatforms();

  const onFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
    async (event) => {
      event.preventDefault();

      if (!formElementRef.current) {
        return;
      }

      const platformSlugs = platforms?.map((platform) => platform.slugName) as [
        string,
      ];

      const formData = new FormData(formElementRef.current);

      const validFormDataObject = match(Object.fromEntries(formData))
        .with(
          { platform: P.union(...platformSlugs), query: P.string },
          (validFormData) => validFormData,
        )
        .otherwise(() => null);

      if (!validFormDataObject) {
        console.warn(
          "Skipping search form submission because form data not valid!",
        );
        return;
      }

      const targetUrl = routeUrls.searchResults({
        ...validFormDataObject,
        localeCode,
      });

      router.push(targetUrl);
    },
    [formElementRef, localeCode, platforms, router],
  );

  return onFormSubmit;
};

export default useSearchFormOnSubmit;
