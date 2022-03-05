import { HTTP_URL } from "./backend";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { LatLng } from "leaflet";

// TODO: We should be auto-generating this from FastAPI's openapi.json.
export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: HTTP_URL }),
  endpoints: (builder) => ({
    getCommitBoundaryForFlight: builder.query<LatLng[], string>({
      query: (flightId) => `flights/${flightId}/commit-boundary`,
    }),
  }),
});

export const { useGetCommitBoundaryForFlightQuery } = apiSlice;
