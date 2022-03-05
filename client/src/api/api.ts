import { HTTP_URL } from "./backend";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { LatLng } from "leaflet";

// TODO: We should be auto-generating this from FastAPI's openapi.json.
export const apiSlice = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: HTTP_URL }),
  tagTypes: ["ControlPoint"],
  endpoints: (builder) => ({
    getCommitBoundaryForFlight: builder.query<LatLng[], string>({
      query: (flightId) => `flights/${flightId}/commit-boundary`,
      providesTags: ["ControlPoint"],
    }),
    setControlPointDestination: builder.mutation<
      void,
      { id: number; destination: LatLng }
    >({
      query: ({ id, destination }) => ({
        url: `control-points/${id}/destination`,
        method: "PUT",
        body: { lat: destination.lat, lng: destination.lng },
        invalidatesTags: ["ControlPoint"],
      }),
    }),
    controlPointCancelTravel: builder.mutation<void, number>({
      query: (id) => ({
        url: `control-points/${id}/cancel-travel`,
        method: "PUT",
        invalidatesTags: ["ControlPoint"],
      }),
    }),
  }),
});

export const {
  useGetCommitBoundaryForFlightQuery,
  useSetControlPointDestinationMutation,
  useControlPointCancelTravelMutation,
} = apiSlice;
