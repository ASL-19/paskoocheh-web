import { createContext } from "react";

const BlogPageContext = createContext<{
  topic: string;
}>({
  topic: "",
});

export default BlogPageContext;
