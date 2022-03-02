import axios from "axios";

export const backend = axios.create({
  baseURL: "http://[::1]:5000/",
});

export const WEBSOCKET_URL = "ws://[::1]:5000/eventstream";

export default backend;
