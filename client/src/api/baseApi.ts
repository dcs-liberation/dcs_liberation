import { HTTP_URL } from "./backend";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseApi = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: HTTP_URL }),
  endpoints: () => ({}),
});
