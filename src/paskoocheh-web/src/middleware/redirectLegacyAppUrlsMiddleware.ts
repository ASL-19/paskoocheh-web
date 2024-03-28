import { NextResponse } from "next/server";

import { LegacyToolUrlParts } from "src/middleware";
import routeUrls from "src/routeUrls";
import { isValidVersionPreview } from "src/types/appTypes";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getValidToolPrimaryToolType from "src/utils/getValidToolPrimaryToolType";

const redirectLegacyAppUrlsMiddleware = async ({
  legacyToolUrlParts,
}: {
  legacyToolUrlParts: LegacyToolUrlParts;
}) => {
  try {
    const graphQlSdk = await getGraphQlSdk();

    const versionPreviewResponse = await graphQlSdk.getVersionPreview({
      platformSlug: legacyToolUrlParts.platformSlug,
      toolPk: legacyToolUrlParts.toolPk,
    });

    const versionPreview = versionPreviewResponse?.version;

    if (!versionPreview) {
      console.warn(
        `[redirectLegacyAppUrlsMiddleware] There is no published version with platformSlug=${legacyToolUrlParts.platformSlug} and toolPk=${legacyToolUrlParts.toolPk}`,
      );
      return;
    }

    const validVersionPreview =
      versionPreview && isValidVersionPreview(versionPreview)
        ? versionPreview
        : null;

    if (!validVersionPreview) {
      console.warn(
        `[redirectLegacyAppUrlsMiddleware] ${
          versionPreview.tool?.name || "Unnamed tool"
        } doesn’t have a primary or first tool type`,
      );
      // As of 2023-11-06 this doesn’t currently change the response status code
      // due to https://github.com/vercel/next.js/issues/48546 (the page will
      // still render with 404 which is acceptable)
      return NextResponse.next({
        status: 500,
      });
    }

    const path = routeUrls.app({
      localeCode: "fa",
      platform: legacyToolUrlParts.platformSlug,
      slug: validVersionPreview.tool.slug,
      toolType: getValidToolPrimaryToolType(validVersionPreview.tool).slug,
    });

    return NextResponse.redirect(
      `${process.env.NEXT_PUBLIC_WEB_URL}${path}`,
      301,
    );
  } catch (err) {
    console.error("[redirectLegacyAppUrlsMiddleware] Error:", err);
  }
};

export default redirectLegacyAppUrlsMiddleware;
