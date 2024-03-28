import {
  StylableFC,
  useFormStateAndFocusManagement,
} from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { FormEventHandler, memo, useCallback, useId, useState } from "react";

import FormErrorMessages from "src/components/form/FormErrorMessages";
import FormSubmitButton from "src/components/form/FormSubmitButton";
import Input from "src/components/form/Input";
import SimpleAppInfo from "src/components/form/SimpleAppInfo";
import StarRatings from "src/components/form/StarRatings";
import TextArea from "src/components/form/TextArea";
import WriteAReviewCategoryRatingListItem from "src/components/form/WriteAReviewCategoryRatingListItem";
import { GqlVersionPreview } from "src/generated/graphQl";
import { useAppStrings } from "src/stores/appStore";
import { formButton, formContainer } from "src/styles/formStyles";
import { paragraphP2SemiBold } from "src/styles/typeStyles";

export type WriteAReviewStrings = {
  categoryRatingsHeading: string;
  overallRatingHeading: string;
  speedReliabilityLabel: string;
};

// ==============
// === Styles ===
// ==============
const formWrapper = css(formContainer, {
  alignItems: "flex-start",
});

const heading = css(paragraphP2SemiBold);

const ratingContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1.5rem",
});

const categoryContainer = css({
  display: "flex",
  flexDirection: "column",
  rowGap: "1rem",
});

const inputGroup = css({ width: "100%" });

const formSubmit = css({ marginLeft: "auto", marginRight: "auto" });

const formErrorMessages = css({
  textAlign: "center",
});

// ==============================
// ===== Next.js component ======
// ==============================
const WriteAReview: StylableFC<{ versionPreview: GqlVersionPreview }> = memo(
  ({ versionPreview }) => {
    const strings = useAppStrings();
    const headingId = useId();

    // handle errors
    const { errorMessagesListRef, formState, setFormState } =
      useFormStateAndFocusManagement();

    const [overallRating, setOverallRating] = useState(0);
    const [speedAndReliabilityRating, setSpeedAndReliabilityRating] =
      useState(0);
    const [miscCategoryRating1, setMiscCategoryRating1] = useState(0);
    const [miscCategoryRating2, setMiscCategoryRating2] = useState(0);
    const [miscCategoryRating3, setMiscCategoryRating3] = useState(0);
    const [miscCategoryRating4, setMiscCategoryRating4] = useState(0);
    const [title, setTitle] = useState("");
    const [message, setMessage] = useState("");

    const onFormSubmit: FormEventHandler<HTMLFormElement> = useCallback(
      async (event) => {
        event.preventDefault();

        setFormState({ type: "isSubmitting" });

        // const titleValue = title ?? "";
        // const messageValue = message ?? "";

        try {
          setFormState({
            type: "isSubmitted",
          });
        } catch {
          setFormState({
            errorMessages: [strings.shared.form.errorMessageGeneric],
            type: "hasErrorMessages",
          });
        }
      },
      [setFormState, strings.shared.form.errorMessageGeneric],
    );

    const onFormInput: FormEventHandler<HTMLFormElement> = useCallback(() => {
      if (formState.type === "hasErrorMessages") {
        setFormState({ type: "isNotSubmitted" });
      }
    }, [formState.type, setFormState]);

    return (
      <form css={formWrapper} onSubmit={onFormSubmit} onInput={onFormInput}>
        <SimpleAppInfo versionPreview={versionPreview} />

        <div css={ratingContainer}>
          <h3 css={heading} id={headingId}>
            {strings.WriteAReview.overallRatingHeading}
          </h3>
          <StarRatings
            setRating={setOverallRating}
            rating={overallRating}
            ariaLabelledBy={headingId}
          />
        </div>

        <div css={ratingContainer}>
          <h3 css={heading}>{strings.WriteAReview.categoryRatingsHeading}</h3>
          <ul css={categoryContainer}>
            <WriteAReviewCategoryRatingListItem
              label={strings.WriteAReview.speedReliabilityLabel}
              rating={speedAndReliabilityRating}
              setRating={setSpeedAndReliabilityRating}
            />
            <WriteAReviewCategoryRatingListItem
              label={strings.WriteAReview.speedReliabilityLabel}
              rating={miscCategoryRating1}
              setRating={setMiscCategoryRating1}
            />
            <WriteAReviewCategoryRatingListItem
              label={strings.WriteAReview.speedReliabilityLabel}
              rating={miscCategoryRating2}
              setRating={setMiscCategoryRating2}
            />
            <WriteAReviewCategoryRatingListItem
              label={strings.WriteAReview.speedReliabilityLabel}
              rating={miscCategoryRating3}
              setRating={setMiscCategoryRating3}
            />
            <WriteAReviewCategoryRatingListItem
              label={strings.WriteAReview.speedReliabilityLabel}
              rating={miscCategoryRating4}
              setRating={setMiscCategoryRating4}
            />
          </ul>
        </div>

        <div css={inputGroup}>
          <Input
            type="text"
            setValue={setTitle}
            label={strings.shared.form.titleLabel}
            placeholder={strings.shared.form.titlePlaceholder}
            required
            value={title}
          />
        </div>
        <div css={inputGroup}>
          <TextArea
            label={strings.shared.form.messageLabel}
            setValue={setMessage}
            placeholder={strings.shared.form.messagePlaceholder}
            required
            value={message}
          />
        </div>

        <div css={formSubmit}>
          <FormSubmitButton
            text={strings.shared.form.submitButton}
            formState={formState}
            css={formButton}
          />
        </div>

        <FormErrorMessages
          css={formErrorMessages}
          errorMessagesListRef={errorMessagesListRef}
          formState={formState}
        />
      </form>
    );
  },
);

WriteAReview.displayName = "WriteAReview";

export default WriteAReview;
