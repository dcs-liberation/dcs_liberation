import axios from "axios";

const backendAddr =
  new URL(window.location.toString()).searchParams.get("server") ??
  "[::1]:16880";

export const HTTP_URL = `http://${backendAddr}/`;

export const backend = axios.create({
  baseURL: HTTP_URL,
});

export const WEBSOCKET_URL = `ws://${backendAddr}/eventstream`;

export default backend;
