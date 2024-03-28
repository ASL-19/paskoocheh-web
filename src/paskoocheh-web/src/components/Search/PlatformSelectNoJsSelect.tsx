import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import ArrowSvg from "src/components/icons/general/ArrowSvg";
import { PlatformSelectGroupInfo } from "src/components/Search/PlatformSelect";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import { useAppLocaleInfo } from "src/stores/appStore";
import getPlatformDisplayNames from "src/utils/getPlatformDisplayNames";

const select = css({
  appearance: "auto",
});

const submitButtonArrow = css({
  height: "1rem",
  width: "1rem",
});

const PlatformSelectNoJsSelect: StylableFC<{
  groupInfos: Array<PlatformSelectGroupInfo>;
}> = memo(({ groupInfos, ...remainingProps }) => {
  const { localeCode } = useAppLocaleInfo();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <div {...remainingProps}>
      <select
        defaultValue={queryOrDefaultPlatformSlug}
        css={select}
        name="platform"
      >
        {groupInfos.map((groupInfo) => (
          <optgroup label={groupInfo.heading} key={groupInfo.heading}>
            {groupInfo.platforms?.map((platform) => (
              <option key={platform.id} value={platform.name}>
                {getPlatformDisplayNames(platform, localeCode)}
              </option>
            ))}
          </optgroup>
        ))}
      </select>

      <button type="submit">
        <ArrowSvg css={submitButtonArrow} direction="down" />
      </button>
    </div>
  );
});

PlatformSelectNoJsSelect.displayName = "PlatformSelectNoJsSelect";

export default PlatformSelectNoJsSelect;
