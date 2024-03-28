import { NextApiHandler } from "next";

import appleTouchIcon180Png from "src/static/favicons/apple-touch-icon-180x180.png";

/**
 * Redirect to the hashed location of apple-touch-icon.png.
 *
 * next.config.js contains a /apple-touch-icon.png → /api/apple-touch-icon-png
 * rewrite rule.
 */
const appleTouchIconPng: NextApiHandler = (req, res) => {
  res.redirect(302, appleTouchIcon180Png.src);
};

export default appleTouchIconPng;
