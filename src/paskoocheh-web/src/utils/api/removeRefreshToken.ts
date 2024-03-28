const removeRefreshToken = () =>
  typeof localStorage !== "undefined"
    ? localStorage.removeItem("refreshToken")
    : null;

export default removeRefreshToken;
