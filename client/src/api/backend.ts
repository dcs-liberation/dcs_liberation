import axios from "axios";

export const backend = axios.create({
  baseURL: "http://[::1]:5000/",
});

export default backend;
