import { StylableFC } from "@asl-19/react-dom-utils";
import { memo } from "react";

import { DateInfo } from "src/hooks/useDateInfo";

const FormattedDate: StylableFC<{ dateInfo: DateInfo }> = memo(
  ({ className, dateInfo }) => (
    <time
      className={className}
      dateTime={dateInfo.iso8601}
      suppressHydrationWarning
    >
      {dateInfo.localeFormatted}
    </time>
  ),
);

FormattedDate.displayName = "FormattedDate";

export default FormattedDate;
