const setRefreshToken = (value: string) =>
  typeof localStorage !== "undefined"
    ? localStorage.setItem("refreshToken", value)
    : null;

export default setRefreshToken;
