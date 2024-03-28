export type RouterEventHandler = (
  url: string,
  { shallow }: { shallow: boolean },
) => void;
