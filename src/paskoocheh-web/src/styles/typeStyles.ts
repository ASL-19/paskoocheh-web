import { devLabel } from "@asl-19/emotion-utils";
import { css } from "@emotion/react";
import { Inter } from "next/font/google";

// Note: some sections of composed styles use array arguments so Prettier
// formats them all the same way (otherwise `css()` call formatting would be
// inconsistent with some calls’ arguments on one line and others on separate
// lines).

export const inter = Inter({
  adjustFontFallback: true,
  display: "swap",
  subsets: ["latin"],
});

export const interRegular = css(inter.style, {
  fontWeight: "400",
});

export const interSemiBold = css(inter.style, {
  fontWeight: "600",
});

export const interBold = css(inter.style, {
  fontWeight: "700",
});

export const interExtraBold = css(inter.style, {
  fontWeight: "800",
});

// ===============
// === Heading ===
// ===============
const headingH1 = css({
  fontSize: "3rem",
  lineHeight: "3.5rem",
});

const headingH1Small = css({
  fontSize: "2.125rem",
  lineHeight: "2.5rem",
});

const headingH2 = css({
  fontSize: "2.438rem",
  lineHeight: "2.938rem",
});

const headingH2Small = css({
  fontSize: "2.062rem",
  lineHeight: "2.5rem",
});

const headingH3 = css({
  fontSize: "2.063rem",
  lineHeight: "2.5rem",
});

const headingH3Small = css({
  fontSize: "1.75rem",
  lineHeight: "2.125rem",
});

const headingH4 = css({
  fontSize: "1.75rem",
  lineHeight: "2.125rem",
});

const headingH4Small = css({
  fontSize: "1.437rem",
  lineHeight: "1.75rem",
});

const headingH5 = css({
  fontSize: "1.438rem",
  lineHeight: "1.75rem",
});

const headingH5Small = css({
  fontSize: "1.187rem",
  lineHeight: "1.437rem",
});

const headingH6 = css({
  fontSize: "1.188rem",
  lineHeight: "1.438rem",
});

const headingH6Small = css({
  fontSize: "1rem",
  lineHeight: "1.187rem",
});

export const headingH1SemiBold = css(
  devLabel("headingH1SemiBold"),
  interSemiBold,
  headingH1,
  { letterSpacing: "-0.04em" },
);

export const headingH1SmallSemiBold = css(
  devLabel("headingH1SmallSemiBold"),
  interSemiBold,
  headingH1Small,
  {
    letterSpacing: "-0.04em",
  },
);

export const headingH1Bold = css(
  devLabel("headingH1Bold"),
  interBold,
  headingH1,
  { letterSpacing: "-0.04em" },
);

export const headingH1SmallBold = css(
  devLabel("headingH1SmallBold"),
  interBold,
  headingH1Small,
  {
    letterSpacing: "-0.04em",
  },
);

export const headingH1ExtraBold = css(
  devLabel("headingH1ExtraBold"),
  interExtraBold,
  headingH1,
  { letterSpacing: "-0.04em" },
);

export const headingH1SmallExtraBold = css(
  devLabel("headingH1SmallExtraBold"),
  interExtraBold,
  headingH1Small,
  {
    letterSpacing: "-0.04em",
  },
);

export const headingH2SemiBold = css(
  devLabel("headingH2SemiBold"),
  interSemiBold,
  headingH2,
  { letterSpacing: "-0.02em" },
);

export const headingH2SmallSemiBold = css(
  devLabel("headingH2SmallSemiBold"),
  interSemiBold,
  headingH2Small,
  { letterSpacing: "-0.02em" },
);

export const headingH2Bold = css(
  devLabel("headingH2Bold"),
  interBold,
  headingH2,
  { letterSpacing: "-0.04em" },
);

export const headingH2SmallBold = css(
  devLabel("headingH2SmallBold"),
  interBold,
  headingH2Small,
  { letterSpacing: "-0.02em" },
);

export const headingH2ExtraBold = css(
  devLabel("headingH2ExtraBold"),
  interExtraBold,
  headingH2,
  { letterSpacing: "-0.04em" },
);

export const headingH2SmallExtraBold = css(
  devLabel("headingH2SmallExtraBold"),
  interExtraBold,
  headingH2Small,
  { letterSpacing: "-0.02em" },
);

export const headingH3SemiBold = css(
  devLabel("headingH3SemiBold"),
  interSemiBold,
  headingH3,
  { letterSpacing: "-0.02em" },
);

export const headingH3SmallSemiBold = css(
  devLabel("headingH3SmallSemiBold"),
  interSemiBold,
  headingH3Small,
  { letterSpacing: "-0.02em" },
);

export const headingH3Bold = css(
  devLabel("headingH3Bold"),
  interBold,
  headingH3,
  { letterSpacing: "-0.02em" },
);

export const headingH3SmallBold = css(
  devLabel("headingH3SmallBold"),
  interBold,
  headingH3Small,
  { letterSpacing: "-0.02em" },
);

export const headingH3ExtraBold = css(
  devLabel("headingH3ExtraBold"),
  interExtraBold,
  headingH3,
  { letterSpacing: "-0.02em" },
);

export const headingH3SmallExtraBold = css(
  devLabel("headingH3SmallExtraBold"),
  interExtraBold,
  headingH3Small,
  { letterSpacing: "-0.02em" },
);

export const headingH4SemiBold = css(
  devLabel("headingH4SemiBold"),
  interSemiBold,
  headingH4,
  { letterSpacing: "-0.02em" },
);

export const headingH4SmallSemiBold = css(
  devLabel("headingH4SemiBold"),
  interSemiBold,
  headingH4Small,
  { letterSpacing: "-0.02em" },
);

export const headingH4Bold = css(
  devLabel("headingH4Bold"),
  interBold,
  headingH4,
  { letterSpacing: "-0.02em" },
);

export const headingH4SmallBold = css(
  devLabel("headingH4SmallBold"),
  interBold,
  headingH4Small,
  { letterSpacing: "-0.02em" },
);

export const headingH4ExtraBold = css(
  devLabel("headingH4ExtraBold"),
  interExtraBold,
  headingH4,
  { letterSpacing: "-0.02em" },
);

export const headingH4SmallExtraBold = css(
  devLabel("headingH4SmallExtraBold"),
  interExtraBold,
  headingH4Small,
  { letterSpacing: "-0.02em" },
);

export const headingH5SemiBold = css(
  devLabel("headingH5SemiBold"),
  interSemiBold,
  headingH5,
  { letterSpacing: "-0.02em" },
);

export const headingH5SmallSemiBold = css(
  devLabel("headingH5SmallSemiBold"),
  interSemiBold,
  headingH5Small,
  { letterSpacing: "-0.02em" },
);

export const headingH5Bold = css(
  devLabel("headingH5Bold"),
  interBold,
  headingH5,
  { letterSpacing: "-0.02em" },
);

export const headingH5SmallBold = css(
  devLabel("headingH5SmallBold"),
  interBold,
  headingH5Small,
  { letterSpacing: "-0.02em" },
);

export const headingH5ExtraBold = css(
  devLabel("headingH5ExtraBold"),
  interExtraBold,
  headingH5,
  { letterSpacing: "-0.02em" },
);

export const headingH5SmallExtraBold = css(
  devLabel("headingH5SmallExtraBold"),
  interExtraBold,
  headingH5Small,
  { letterSpacing: "-0.02em" },
);

export const headingH6SemiBold = css(
  devLabel("headingH6SemiBold"),
  interSemiBold,
  headingH6,
  { letterSpacing: "-0.02em" },
);

export const headingH6SmallSemiBold = css(
  devLabel("headingH6SmallSemiBold"),
  interSemiBold,
  headingH6Small,
  { letterSpacing: "-0.02em" },
);

export const headingH6Bold = css(
  devLabel("headingH6Bold"),
  interBold,
  headingH6,
  { letterSpacing: "-0.02em" },
);

export const headingH6SmallBold = css(
  devLabel("headingH6SmallBold"),
  interBold,
  headingH6Small,
  { letterSpacing: "-0.02em" },
);

export const headingH6ExtraBold = css(
  devLabel("headingH6ExtraBold"),
  interExtraBold,
  headingH6,
  { letterSpacing: "-0.02em" },
);

export const headingH6SmallExtraBold = css(
  devLabel("headingH6SmallExtraBold"),
  interExtraBold,
  headingH6Small,
  { letterSpacing: "-0.02em" },
);

// ==================
// === Subheading ===
// ==================
const subheading = css({
  fontSize: "1.25rem",
  lineHeight: "1.5rem",
});

export const subheadingRegular = css(
  devLabel("subheadingRegular"),
  interRegular,
  subheading,
);

export const subheadingSemiBold = css(
  devLabel("subheadingSemiBold"),
  interSemiBold,
  subheading,
);

export const subheadingUnderline = css(
  devLabel("subheadingUnderline"),
  interRegular,
  subheading,
  { textDecoration: "underline" },
);

// =================
// === Paragraph ===
// =================
const paragraphP1 = css({
  fontSize: "0.875rem",
  lineHeight: "1.063rem",
});

const paragraphP2 = css({
  fontSize: "1rem",
  lineHeight: "1.188rem",
});

const paragraphP3 = css({
  fontSize: "1.125rem",
  lineHeight: "1.35rem",
});

export const paragraphP1Regular = css(
  devLabel("paragraphP1Regular"),
  interRegular,
  paragraphP1,
);

export const paragraphP1SemiBold = css(
  devLabel("paragraphP1SemiBold"),
  interSemiBold,
  paragraphP1,
);

export const paragraphP1Underline = css(
  devLabel("paragraphP1Underline"),
  interRegular,
  paragraphP1,
  { textDecoration: "underline" },
);

export const paragraphP2Regular = css(
  devLabel("paragraphP2Regular"),
  interRegular,
  paragraphP2,
);

export const paragraphP2SemiBold = css(
  devLabel("paragraphP2SemiBold"),
  interSemiBold,
  paragraphP2,
);

export const paragraphP2Underline = css(
  devLabel("paragraphP2Underline"),
  interRegular,
  paragraphP2,
  { textDecoration: "underline" },
);

export const paragraphP3Regular = css(
  devLabel("paragraphP3Regular"),
  interRegular,
  paragraphP3,
);

export const paragraphP3SemiBold = css(
  devLabel("paragraphP3SemiBold"),
  interSemiBold,
  paragraphP3,
);

export const paragraphP3Underline = css(
  devLabel("paragraphP3Underline"),
  interRegular,
  paragraphP3,
  { textDecoration: "underline" },
);

// ===============
// === Caption ===
// ===============
const caption = css({
  fontSize: "0.75rem",
  lineHeight: "0.875rem",
});

export const captionRegular = css([
  devLabel("captionRegular"),
  interRegular,
  caption,
]);

export const captionSemiBold = css([
  devLabel("captionSemiBold"),
  interSemiBold,
  caption,
]);

export const captionCap = css([
  devLabel("captionCap"),
  interSemiBold,
  caption,
  { letterSpacing: "0.08rem" },
]);

// ==============
// === Footer ===
// ==============

const footer = css([
  devLabel("footerCap"),
  {
    fontSize: "0.625rem",
    letterSpacing: "0.02rem",
    lineHeight: "0.75rem",
  },
]);

export const footerRegular = css([
  devLabel("footerRegular"),
  interRegular,
  footer,
]);

export const footerSemiBold = css([
  devLabel("footerSemiBold"),
  interSemiBold,
  footer,
]);

export const footerCap = css([
  devLabel("footerCap"),
  interSemiBold,
  footer,
  { letterSpacing: "0.08rem" },
]);

// ==============
// === Display ===
// ==============

export const display01Semibold = css([
  devLabel("display01SemiBold"),
  interSemiBold,
  {
    fontSize: "4.5rem",
    letterSpacing: "-0.04rem",
    lineHeight: "5rem",
  },
]);
