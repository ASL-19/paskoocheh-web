import { NextApiHandler } from "next";

import faviconIcoStaticImageData from "src/static/favicons/favicon.ico";

/**
 * Redirect to the hashed location of favicon.ico.
 *
 * next.config.js contains a /favicon.ico → /api/favicon-ico rewrite rule.
 */
const faviconIco: NextApiHandler = (req, res) => {
  res.redirect(302, faviconIcoStaticImageData.src);
};

export default faviconIco;
