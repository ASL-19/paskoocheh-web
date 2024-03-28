import { useAppLocaleInfo } from "src/stores/appStore";

export type DateInfo = {
  date: Date;
  iso8601: string;
  localeFormatted: string;
};

const useDateInfo = ({ dateString }: { dateString: string | null }) => {
  const { dateTimeFormatter } = useAppLocaleInfo();

  const date = new Date(dateString || "");

  if (!(date instanceof Date) || isNaN(date.getTime())) {
    return null;
  }

  const iso8601 = date.toISOString().substring(0, 10);

  const localeFormatted = dateTimeFormatter.format(date);

  if (!dateString) {
    return null;
  }

  return {
    date,
    iso8601,
    localeFormatted,
  } as DateInfo;
};

export default useDateInfo;
