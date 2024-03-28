const getRefreshToken = () =>
  typeof localStorage !== "undefined"
    ? localStorage.getItem("refreshToken")
    : null;

export default getRefreshToken;
