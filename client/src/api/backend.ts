import axios from "axios";

const backendAddr =
  new URL(window.location.toString()).searchParams.get("server") ??
  "[::1]:16880";

// MSW can't handle IPv6 URLs...
// https://github.com/mswjs/msw/issues/1388
export const HTTP_URL =
  process.env.NODE_ENV === "test" ? "" : `http://${backendAddr}/`;

export const backend = axios.create({
  baseURL: HTTP_URL,
});

export const WEBSOCKET_URL = `ws://${backendAddr}/eventstream`;

export default backend;
