import { match, P } from "ts-pattern";

import { ValidTool, ValidToolPreview } from "src/types/appTypes";
import { unknownToolTypeSlug } from "src/values/apiValues";

const getValidToolPrimaryToolType = (tool: ValidTool | ValidToolPreview) =>
  match(tool)
    .with(
      { primaryTooltype: { slug: P.not(unknownToolTypeSlug) } },
      (toolType) => toolType.primaryTooltype,
    )
    .otherwise(() => tool.toolTypes[0]);

export default getValidToolPrimaryToolType;
