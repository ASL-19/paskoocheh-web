import { createContext } from "react";

const HomePageContext = createContext<{
  category: string | undefined;
}>({
  category: "",
});

export default HomePageContext;
