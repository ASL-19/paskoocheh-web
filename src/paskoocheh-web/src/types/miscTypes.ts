import { KeenSliderHooks, KeenSliderInstance } from "keen-slider/react";
import { FC, MutableRefObject } from "react";

import { GqlDownloadOptions } from "src/generated/graphQl";

export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;

export type HeadingTagName = "h1" | "h2" | "h3" | "h4" | "h5" | "h6";

export type FetchPriority = "high" | "low" | "auto";

export type VideoType = "youtube" | "video";

export type FaqInfo = {
  answer: string;
  id: string;
  question: string;
};

export type FilterLinkInfo = {
  id: string;
  name: string;
  url: string;
};

export type EventsInfo = {
  date: string;
  description: string;
  id: number;
  image: string;
  publisher: string;
  publisherImg: string | null;
  slug: string;
  time: string;
  title: string;
  type: string;
};

export type RouteInfo = {
  key: string;
  name: string;
  route: string;
};

export type SocialLinks = {
  facebook: string;
  telegram: string;
  twitter: string;
};

export type AboutImage = {
  alt: string;
  id: string;
  image: string;
};

export type BlockInfo = {
  description: string;
  id?: string;
  title: string;
};

export type ProjectInfo = {
  description: string;
  detailDescription: {
    author: string;
    position: string;
    quotation: string;
    text: string;
    title: string;
  };
  id: string;
  image: string;
  issues: Array<{
    id: string;
    name: string;
    slug: string;
  }>;
  launchDate: string;
  partner: {
    id: string;
    name: string;
    url: string;
  };
  perform: Array<{
    name: string;
  }>;
  results: {
    coverage: number;
    interactions: number;
    static: number;
    summary: string;
  };
  slug: string;
  socialUsernames: {
    facebook?: string;
    instagram?: string;
    telegram?: string;
    twitter?: string;
  };
  synopsis: string;
  title: string;
  url: string;
};

export type ServiceInfo = {
  IconComponent: FC<{ className?: string }>;
  description: string;
  id?: string;
  title: string;
};

export type LeadershipInfo = {
  email: string;
  id: string;
  image: string;
  name: string;
  pgp: string;
  title: string;
  twitterUrl: string;
};

export type RatingInfo = {
  id: string;
  name: string;
  rating: number;
};

export type TeamAnalysis = {
  averageTeamRating: number;
  categoryRatings: Array<RatingInfo>;
  cons: Array<{
    description: string;
  }>;
  pros: Array<{
    description: string;
  }>;
  reviews: string;
};

export type UserReview = {
  description: string;
  id: string;
  published: string;
  starRating: number;
  title: string;
  votes: {
    thumbDown: number;
    thumbUp: number;
  };
};

export type UsersRatingsAndReviews = {
  averageUsersRating: number;
  categoryRatings: Array<RatingInfo>;
  reviews: Array<UserReview>;
};

export type VideoInfo = {
  height: number;
  id: string;
  title: string;
  type: VideoType;
  url: string;
  videoCode: string;
  width: number;
};

export type AdditionalInfo = {
  description: string;
  id: string;
  title: string;
};

export type InstallationOption = {
  downloadUrl: string;
  name: string;
  slug: GqlDownloadOptions | "EMAIL";
};

export type AppInfo = {
  developerName: string;
  image: string;
  images: Array<{
    id: string;
    image: string;
  }>;
  installationOptions: Array<InstallationOption>;
  name: string;
  operatingSystems: {
    android: boolean;
    chrome: boolean;
    firefox: boolean;
    ios: boolean;
    linux: boolean;
    macos: boolean;
    windows: boolean;
  };
  pk: number;
  primaryTooltype: {
    icon: string;
    id: string;
    name: string;
    nameFa: string;
    pk: number;
    slug: string;
  } | null;
  slug: string;
  stats: {
    android: string;
    downloads: number;
    reviews: number;
    stars: number;
  };
  teamAnalysis: TeamAnalysis;
  toolTypes: Array<{
    icon: string;
    id: string;
    name: string;
    nameFa: string;
    slug: string;
  }>;
  usersReviews: UsersRatingsAndReviews;
};

export type HowToUseInfo = {
  description: string;
  video: VideoInfo;
};

export type IconDirection = "up" | "start" | "down" | "end";

export type KeenSliderRef = MutableRefObject<KeenSliderInstance<
  {},
  {},
  KeenSliderHooks
> | null>;
