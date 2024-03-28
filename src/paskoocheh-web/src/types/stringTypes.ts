import { A11yShortcutPresetStrings } from "src/components/A11yShortcutPreset";
import { DeleteAccountOverlayStrings } from "src/components/AccountSettings/DeleteAccountOverlay";
import { AppAdditionalInfoListItemStrings } from "src/components/App/AppTabContent/AppAdditionalInfo/AppAdditionalInfoListItem";
import { AppAdditionalInfoProductDetailsStrings } from "src/components/App/AppTabContent/AppAdditionalInfo/AppAdditionalInfoProductDetails";
import { AppDetailsSectionStrings } from "src/components/App/AppTabContent/AppDetailsSection";
import { AppFaqsStrings } from "src/components/App/AppTabContent/AppFaqs/AppFaqs";
import { AppHowToUseStrings } from "src/components/App/AppTabContent/AppHowToUse/AppHowToUse";
import { AppNavLinkListStrings } from "src/components/App/AppTabContent/AppNavLinkList";
import { AppUsersReviewsContentStrings } from "src/components/App/AppTabContent/AppRatingsAndReviews/AppUsersReviewsContent";
import { AppTeamAnalysisStrings } from "src/components/App/AppTabContent/AppTeamAnalysis/AppTeamAnalysis";
import { AppTeamReviewsContentStrings } from "src/components/App/AppTabContent/AppTeamAnalysis/AppTeamReviewsContent";
import { AppAndroidInstallButtonStrings } from "src/components/App/AppTopHeaderAndScreenshots/AppAndroidInstallButton";
import { AppInstallOptionsStrings } from "src/components/App/AppTopHeaderAndScreenshots/AppInstallOptions";
import { AppOverviewSectionStrings } from "src/components/App/AppTopHeaderAndScreenshots/AppOverviewSection";
import { AppShareAndSupportLinksStrings } from "src/components/App/AppTopHeaderAndScreenshots/AppShareAndSupportLinks";
import { AppStatsDetailsStrings } from "src/components/App/AppTopHeaderAndScreenshots/AppStatsDetails";
import { BlogPostContentStrings } from "src/components/BlogPage/BlogPostContent";
import { CategoryNavListStrings } from "src/components/CategoryNavList";
import { ClientSideErrorFallbackStrings } from "src/components/ClientSideErrorFallback";
import { CreateAnAccountReferralMessageStrings } from "src/components/CreateAnAccountPage/CreateAnAccountReferralMessage";
import { ErrorPageContentStrings } from "src/components/ErrorPageContent";
import { FooterStrings } from "src/components/Footer/Footer";
import { FooterNavStrings } from "src/components/Footer/FooterNav";
import { FooterNewsletterSignUpStrings } from "src/components/Footer/FooterNewsletterSignUp";
import { StarRatingsStrings } from "src/components/form/StarRatings";
import { WriteAReviewStrings } from "src/components/form/WriteAReview";
import { HeaderStrings } from "src/components/Header/Header";
import { MobileHeaderNavDropdownStrings } from "src/components/Header/MobileHeaderNavDropdown";
import { MobileHeaderNavMenuButtonStrings } from "src/components/Header/MobileHeaderNavMenuButton";
import { SearchStrings } from "src/components/Header/SearchBox";
import { HomePageEditorsChoiceSegmentStrings } from "src/components/HomePage/HomePageEditorsChoiceSegment";
import { HomePagePopularAppsSegmentStrings } from "src/components/HomePage/HomePagePopularAppsSegment";
import { IndexPageLoadingUiStrings } from "src/components/IndexPageLoadingUi";
import { NoResultsIllustrationAndMessageStrings } from "src/components/NoResultsIllustrationAndMessage";
import { OverallRatingsStrings } from "src/components/OverallRatings";
import { PageMetaStrings } from "src/components/Page/PageMeta";
import { HowPointsWorkStrings } from "src/components/RewardsPage/HowPointsWork";
import { RewardsReferralLinkStrings } from "src/components/RewardsPage/RewardsDashboard/RewardsReferralLink";
import { RedemptionOverlayStrings } from "src/components/RewardsPage/RewardsRedemption/RedemptionOverlay";
import { RewardsReviewStrings } from "src/components/RewardsPage/RewardsReview/RewardsReview";
import { RewardsWeeklyChallengeStrings } from "src/components/RewardsPage/RewardsWeeklyChallenge/RewardsWeeklyChallenge";
import { PlatformSelectStrings } from "src/components/Search/PlatformSelect";
import { AccessDeniedStrings } from "src/components/UserAccess/AccessDenied";
import { AccessErrorMessageStrings } from "src/components/UserAccess/AccessErrorMessage";
import { AccountSettingsConfirmationPageStrings } from "src/pageComponents/AccountSettingsConfirmationPage/AccountSettingsConfirmationPage";
import { AccountSettingsPageContentStrings } from "src/pageComponents/AccountSettingsPage/AccountSettingsPageContent";
import { ActivateAccountPageStrings } from "src/pageComponents/ActivateAccountPage/ActivateAccountPage";
import { BlogPageStrings } from "src/pageComponents/BlogPage/BlogPage";
import { ContactPageStrings } from "src/pageComponents/ContactPage/ContactPage";
import { CreateAnAccountPageStrings } from "src/pageComponents/CreateAnAccountPage/CreateAnAccountPage";
import { HomePageStrings } from "src/pageComponents/HomePage/HomePage";
import { HowPointsWorkPageStrings } from "src/pageComponents/HowPointsWorkPage/HowPointsWorkPage";
import { ResetPasswordPageStrings } from "src/pageComponents/ResetPasswordPage/ResetPasswordPage";
import { ResetPasswordRequestPageStrings } from "src/pageComponents/ResetPasswordRequestPage/ResetPasswordRequestPage";
import { RewardsPageContentStrings } from "src/pageComponents/RewardsPage/RewardsPageContent";
import { SearchResultsPageStrings } from "src/pageComponents/SearchResultsPage/SearchResultsPage";
import { SignInPageStrings } from "src/pageComponents/SignInPage/SignInPage";
import { WriteAReviewPageStrings } from "src/pageComponents/WriteAReviewPage/WriteAReviewPage";
import { WriteYourMessagePageStrings } from "src/pageComponents/WriteYourMessagePage/WriteYourMessagePage";

export type SharedStrings = {
  /**
   * Accessibility announcements. Used when loading new items in the listing
   * pages.
   */
  a11yAnnouncements: {
    /**
     * Read by screen reader when finished loading new list items.
     *
     * "\{count\}" is replaced by the number of new items loaded.
     */
    loadingNewItemsComplete: string;

    /**
     * Read by screen reader when beginning to load new list items.
     */
    loadingNewItemsStarted: string;
  };

  /**
   * "All" string used in various places (e.g. category/topic nav lists).
   */
  all: string;

  /**
   * Shared strings for button
   */
  button: {
    getStarted: string;
    goToHomePage: string;
    learnMore: string;
    more: string;
    next: string;
    notEnoughPoints: string;
    redeem: string;
    resetPassword: string;
    send: string;
    signIn: string;
    submit: string;
  };

  /**
   * Shared strings for rewards dashboard
   */
  dashboard: {
    errorMessages: {
      default: string;
    };
  };

  /**
   * Shared strings for dialogs/menus
   */
  dialog: {
    a11yCloseButton: string;
  };

  /**
   * "Download now" button text
   */
  downloadNow: string;

  errorMessages: {
    networkError: string;
    videoError: string;
  };

  /**
   * Shared Text for forms
   */
  form: {
    emailLabel: string;
    emailPlaceholder: string;
    errorMessageGeneric: string;
    errorMessages: {
      /**
       * Displayed if form submission failed due to network error.
       */
      network: string;

      /**
       * Displayed if form submission failed due to unknown error.
       */
      unknown: string;
    };
    messageLabel: string;
    messagePlaceholder: string;
    submitButton: string;
    titleLabel: string;
    titlePlaceholder: string;
  };

  googleDownloadButton: string;

  /**
   * "Learn more" button text
   */
  learnMore: string;

  // "Load more" button text
  loadMoreLinkText: string;

  /**
   * Nav links strings
   */
  navLinks: {
    about: string;
    account: {
      accountSettings: string;
      logOut: string;
      signInOrRegister: string;
    };
    app: string;
    blog: string;
    rewards: string;
  };

  /**
   * Message explaining why interactive features require JavaScript and a modern
   * browser to work.
   *
   * Displays if the user has disabled JavaScript, or if they’re using an older
   * browser that doesn’t support the site’s JavaScript code.
   */
  noJsMessage: string;

  operatingSystemsNames: {
    android: string;
  };

  /**
   * Shared string "Read More" button text.
   */
  readMore: string;

  /**
   * Shared string "See More" button text.
   */
  seeMore: string;

  /**
   * Site title (reused where appropriate).
   */
  siteTitle: string;

  /**
   * Skip to main content accessibility text. Used for hidden accessibility
   * shortcuts.
   */
  skipToMainContent: string;

  /**
   * Names of social media platforms.
   */
  socialMediaPlatformNames: {
    email: string;
    facebook: string;
    instagram: string;
    telegram: string;
    twitter: string;
  };

  /**
   * Paskoocheh social media usernames.
   */
  socialMediaUsernames: {
    email: string;
    facebook: string;
    instagram: string;
    telegram: string;
    twitter: string;
  };
};

export type Strings = {
  $schema: string;

  /**
   * Accessibility shortcut preset.
   *
   * These accessibility shortcuts appear when using keyboard or screen reader
   * navigation.
   */
  A11yShortcutPreset: A11yShortcutPresetStrings;

  /**
   * UserAccess - Access denied
   */
  AccessDenied: AccessDeniedStrings;

  /**
   * UserAccess - AccessErrorMessage
   */
  AccessErrorMessage: AccessErrorMessageStrings;

  /**
   * AccountSettingsConfirmationPage
   */
  AccountSettingsConfirmationPage: AccountSettingsConfirmationPageStrings;

  /**
   * Account Setting Page Content
   */
  AccountSettingsPageContent: AccountSettingsPageContentStrings;

  /**
   * ActivateAccountPage
   */
  ActivateAccountPage: ActivateAccountPageStrings;

  /**
   * AppAdditionalInfoLIstItem
   */
  AppAdditionalInfoListItem: AppAdditionalInfoListItemStrings;

  /**
   * AppAdditionalInfoProductDetails
   */
  AppAdditionalInfoProductDetails: AppAdditionalInfoProductDetailsStrings;

  /**
   * App detail page Get it on Paskoocheh Button
   */
  AppAndroidInstallButton: AppAndroidInstallButtonStrings;

  /**
   * App page tabbed details section.
   */
  AppDetailsSection: AppDetailsSectionStrings;

  /**
   * AppFaq
   */
  AppFaqs: AppFaqsStrings;

  /**
   * AppHowToUse component
   */
  AppHowToUse: AppHowToUseStrings;

  /**
   * AppPage - AppInstallOptions
   */
  AppInstallOptions: AppInstallOptionsStrings;

  /**
   * App page detail section links.
   */
  AppNavLinkList: AppNavLinkListStrings;

  /**
   * AppOverviewSection component
   */
  AppOverviewSection: AppOverviewSectionStrings;

  /**
   * App page share and support links (at top corner).
   */
  AppShareAndSupportLinks: AppShareAndSupportLinksStrings;

  /**
   * App page top stats area (containing review count, download count, supported
   * platform version, etc.).
   */
  AppStatsDetails: AppStatsDetailsStrings;

  /**
   * AppTeamAnalysis
   */
  AppTeamAnalysis: AppTeamAnalysisStrings;

  /**
   * AppTeamReviewsContent component
   */
  AppTeamReviewsContent: AppTeamReviewsContentStrings;

  /**
   * AppUsersReviewsContent component
   */
  AppUsersReviewsContent: AppUsersReviewsContentStrings;

  /**
   * Blog page.
   */
  BlogPage: BlogPageStrings;

  /**
   * BlogPostPage BlogPostContent Section
   */
  BlogPostContent: BlogPostContentStrings;

  /**
   * Home page categories nav.
   */
  CategoryNavList: CategoryNavListStrings;

  /**
   * Error view that appears if there’s an unrecoverable error while the browser
   * is rendering the page.
   */
  ClientSideErrorFallback: ClientSideErrorFallbackStrings;

  /**
   * Contact page.
   */
  ContactPage: ContactPageStrings;

  /**
   * Create an account page.
   */
  CreateAnAccountPage: CreateAnAccountPageStrings;

  /**
   * CreateAnAccountPage - CreateAnAccountReferralMessage
   */
  CreateAnAccountReferralMessage: CreateAnAccountReferralMessageStrings;

  /**
   * DeleteAccountOverlay component.
   */
  DeleteAccountOverlay: DeleteAccountOverlayStrings;

  /**
   * Error page.
   *
   * Appears for non-existent pages, and when a page encounters an error.
   */
  ErrorPageContent: ErrorPageContentStrings;

  /**
   * Footer component.
   */
  Footer: FooterStrings;

  /**
   * Footer navigation links (“Contact Us” and “More Information”).
   */
  FooterNav: FooterNavStrings;

  /**
   * Newsletter SignUp component
   */
  FooterNewsletterSignUp: FooterNewsletterSignUpStrings;

  /**
   * Header component.
   */
  Header: HeaderStrings;

  /**
   * Home page.
   */
  HomePage: HomePageStrings;

  /**
   * Home “Editor’s choice” section.
   */
  HomePageEditorsChoiceSegment: HomePageEditorsChoiceSegmentStrings;

  /**
   * Home “Popular apps” section.
   */
  HomePagePopularAppsSegment: HomePagePopularAppsSegmentStrings;

  /**
   * RewardsPage - HowPointsWork
   */
  HowPointsWork: HowPointsWorkStrings;

  /**
   * HowPointsWorkPage
   */
  HowPointsWorkPage: HowPointsWorkPageStrings;

  /**
   * Index page “load more” link, loading indicator, and error messages.
   */
  IndexPageLoadingUi: IndexPageLoadingUiStrings;

  /**
   * Mobile nav open/close button.
   * Mobile navigation menu.
   */
  MobileHeaderNavDropdown: MobileHeaderNavDropdownStrings;

  /**
   * Mobile navigation menu open/close button.
   */
  MobileHeaderNavMenuButton: MobileHeaderNavMenuButtonStrings;

  /**
   * No results illustration and message.
   *
   * Appears on index pages when no matched items are found.
   */
  NoResultsIllustrationAndMessage: NoResultsIllustrationAndMessageStrings;

  /**
   * OverallRatings component
   */
  OverallRatings: OverallRatingsStrings;

  /**
   * Page metadata (including SEO and social media tags).
   */
  PageMeta: PageMetaStrings;

  /**
   * Header platform select menu.
   */
  PlatformSelect: PlatformSelectStrings;

  /**
   * RedemptionOverlay
   */
  RedemptionOverlay: RedemptionOverlayStrings;

  /**
   * ResetPasswordPage
   */
  ResetPasswordPage: ResetPasswordPageStrings;

  /**
   * ResetPasswordRequestPage
   */
  ResetPasswordRequestPage: ResetPasswordRequestPageStrings;

  /**
   * Rewards Page
   */
  RewardsPageContent: RewardsPageContentStrings;

  /**
   * Rewards page referral link.
   */
  RewardsReferralLink: RewardsReferralLinkStrings;

  /**
   * Rewards Page - RewardsMyReview
   */
  RewardsReview: RewardsReviewStrings;

  /**
   * Rewards Page - RewardsWeeklyChallenge
   */
  RewardsWeeklyChallenge: RewardsWeeklyChallengeStrings;

  /**
   * Header Search component
   */
  Search: SearchStrings;

  /**
   * SearchResultsPage
   */
  SearchResultsPage: SearchResultsPageStrings;

  /**
   * Sign In page.
   */
  SignInPage: SignInPageStrings;

  /**
   * Review form rating stars.
   */
  StarRatings: StarRatingsStrings;

  /**
   * Write a review form.
   */
  WriteAReview: WriteAReviewStrings;

  /**
   * Write A Review page.
   */
  WriteAReviewPage: WriteAReviewPageStrings;

  /*
   * Write your message page
   */
  WriteYourMessagePage: WriteYourMessagePageStrings;

  /**
   * [PHASES 1-3] Shared (reused in several components).
   */
  shared: SharedStrings;
};

// Via https://stackoverflow.com/a/47058976/7949868

type Join<T extends Array<string>, D extends string> = T extends []
  ? never
  : T extends [infer F]
    ? F
    : T extends [infer F, ...infer R]
      ? F extends string
        ? `${F}${D}${Join<Extract<R, Array<string>>, D>}`
        : never
      : string;

type PathsToStringProps<T> = T extends string
  ? []
  : {
      [K in Extract<keyof T, string>]: [K, ...PathsToStringProps<T[K]>];
    }[Extract<keyof T, string>];

export type StringKey = Join<PathsToStringProps<Strings>, ".">;
