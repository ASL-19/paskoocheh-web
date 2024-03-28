import {
  Combobox,
  ComboboxPopover,
  useComboboxStore,
} from "@ariakit/react/combobox";
import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { matchSorter } from "match-sorter";
import {
  memo,
  MouseEventHandler,
  RefObject,
  useCallback,
  useDeferredValue,
  useMemo,
  useRef,
} from "react";

import CrossSvg from "src/components/icons/general/CrossSvg";
import SearchSvg from "src/components/icons/general/SearchSvg";
import SearchListItem from "src/components/Search/SearchListItem";
import { useAppStrings } from "src/stores/appStore";
import { useAppLocaleInfo } from "src/stores/appStore";
import { paragraphP1Regular } from "src/styles/typeStyles";
import { isValidVersionPreview, ValidVersionPreview } from "src/types/appTypes";
import { Direction } from "src/types/layoutTypes";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const inputContainer = ({ direction }: { direction: Direction }) =>
  css(
    {
      backgroundColor: colors.secondary50,
      borderRadius:
        direction === "ltr" ? "0 6.25rem 6.25rem 0" : "6.25rem 0 0 6.25rem",
      display: "flex",
      flexGrow: "1",
      paddingInlineEnd: "0.875rem",
    },
    breakpointStyles({
      singleColumn: {
        lt: {
          borderRadius: " 6.25rem",
          flexDirection: "row-reverse",
          paddingInlineStart: "0.875rem",
        },
      },
    }),
  );

const input = css(paragraphP1Regular, {
  color: colors.secondary500,
  flexGrow: "1",
  order: 2,
  textIndent: "1rem",
});

const comboBoxContainer = css({
  backgroundColor: colors.shadesWhite,
  borderRadius: "0.5rem",
  boxShadow: "0 0.75rem 1.5rem rgba(0, 0, 0, 0.1)",
  display: "flex",
  flexDirection: "column",
  maxHeight: "18.75rem",
  overflow: "auto",
  overscrollBehavior: "contain",
  paddingBlock: "1.25rem",
  rowGap: "0.75rem",
});

const iconButton = css({
  alignSelf: "center",
  color: colors.secondary400,
  display: "flex",
});

const submitButton = css(iconButton, {
  order: 3,
});

const clearButton = css(
  iconButton,
  {
    order: 1,
  },
  breakpointStyles({
    singleColumn: {
      gte: {
        marginInlineEnd: "0.5rem",
        order: 2,
      },
    },
  }),
);

const icon = css({
  height: "1rem",
  width: "1rem",
});

// ==============================
// ===== Next.js component ======
// ==============================
const SearchInput: StylableFC<{
  comboboxInputElementRef?: RefObject<HTMLInputElement>;
  comboboxInputId?: string;
  focusComboboxInputElementOnClear?: boolean;
  onClearButtonClick?: () => void;
  versionPreviews: Array<ValidVersionPreview>;
}> = memo(
  ({
    comboboxInputElementRef,
    comboboxInputId,
    focusComboboxInputElementOnClear = false,
    onClearButtonClick,
    versionPreviews,
    ...remainingProps
  }) => {
    const strings = useAppStrings();
    const { direction } = useAppLocaleInfo();

    const combobox = useComboboxStore();
    const state = combobox.useState();
    const deferredSearchInput = useDeferredValue(state.value);

    const internalComboboxInputElementRef = useRef<HTMLInputElement>(null);

    const comboboxValue = combobox.useState("value");

    const matches = useMemo(() => {
      if (!deferredSearchInput) {
        return [];
      }

      const matches = matchSorter(versionPreviews, deferredSearchInput, {
        keys: ["tool.name"],
      });

      return matches;
    }, [deferredSearchInput, versionPreviews]);

    const searchListItems = useMemo(
      () =>
        matches?.reduce(
          (acc, app) =>
            isValidVersionPreview(app)
              ? [...acc, <SearchListItem versionPreview={app} key={app.id} />]
              : acc,
          [],
        ),
      [matches],
    );

    const onClearButtonClickCombined = useCallback<
      MouseEventHandler<HTMLButtonElement>
    >(
      (event) => {
        event.preventDefault();

        const comboboxInputElement =
          comboboxInputElementRef?.current ??
          internalComboboxInputElementRef.current;

        if (comboboxInputElement) {
          combobox.setValue("");

          if (focusComboboxInputElementOnClear) {
            comboboxInputElement.focus();
          }
        }

        if (onClearButtonClick) {
          onClearButtonClick();
        }
      },
      [
        combobox,
        comboboxInputElementRef,
        focusComboboxInputElementOnClear,
        onClearButtonClick,
      ],
    );

    return (
      <div css={inputContainer({ direction })} {...remainingProps}>
        <Combobox
          store={combobox}
          placeholder={strings.Search.inputPlaceholder}
          css={input}
          id={comboboxInputId}
          name="query"
          autoComplete="both"
          ref={comboboxInputElementRef ?? internalComboboxInputElementRef}
        />

        <ComboboxPopover store={combobox} gutter={16} sameWidth={true}>
          {searchListItems.length > 0 && (
            <div css={comboBoxContainer}>{searchListItems}</div>
          )}
        </ComboboxPopover>

        <button
          css={submitButton}
          type="submit"
          aria-label={strings.Search.submitButtonAriaLabel}
        >
          <SearchSvg css={icon} />
        </button>

        {comboboxValue && (
          <button
            css={clearButton}
            onClick={onClearButtonClickCombined}
            type="reset"
          >
            <CrossSvg css={icon} />
          </button>
        )}
      </div>
    );
  },
);

SearchInput.displayName = "SearchInput";

export default SearchInput;
