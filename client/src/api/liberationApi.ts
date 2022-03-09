import { _liberationApi } from "./_liberationApi";

// See https://redux-toolkit.js.org/rtk-query/usage/automated-refetching for an
// explanation of tag behavior.

export enum Tags {
  FLIGHT_PLAN = "FlightPlan",
}

const LIST_ID = "LIST";

function providesList<R extends { id: string | number }[], T extends string>(
  resultsWithIds: R | undefined,
  tagType: T
) {
  return resultsWithIds
    ? [
        { type: tagType, id: LIST_ID },
        ...resultsWithIds.map(({ id }) => ({ type: tagType, id })),
      ]
    : [{ type: tagType, id: LIST_ID }];
}

export const liberationApi = _liberationApi.enhanceEndpoints({
  addTagTypes: Object.values(Tags),
  endpoints: {
    // /debug/waypoint-geometries
    getDebugHoldZones: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    getDebugIpZones: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    getDebugJoinZones: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    // /flights/
    getCommitBoundaryForFlight: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    getFlightById: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    listFlights: {
      providesTags: (result) => providesList(result, Tags.FLIGHT_PLAN),
    },
    // /waypoints/
    listAllWaypointsForFlight: {
      providesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
    setWaypointPosition: {
      invalidatesTags: (result, error, arg) => [
        { type: Tags.FLIGHT_PLAN, id: arg.flightId },
      ],
    },
  },
});

export * from "./_liberationApi";
