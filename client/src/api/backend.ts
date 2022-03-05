import axios from "axios";

export const HTTP_URL = "http://[::1]:5000/";

export const backend = axios.create({
  baseURL: HTTP_URL,
});

export const WEBSOCKET_URL = "ws://[::1]:5000/eventstream";

export default backend;
