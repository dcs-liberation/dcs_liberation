import { baseApi as api } from "./baseApi";

const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    listControlPoints: build.query<
      ListControlPointsApiResponse,
      ListControlPointsApiArg
    >({
      query: () => ({ url: `/control-points/` }),
    }),
    getControlPointById: build.query<
      GetControlPointByIdApiResponse,
      GetControlPointByIdApiArg
    >({
      query: (queryArg) => ({ url: `/control-points/${queryArg.cpId}` }),
    }),
    controlPointDestinationInRange: build.query<
      ControlPointDestinationInRangeApiResponse,
      ControlPointDestinationInRangeApiArg
    >({
      query: (queryArg) => ({
        url: `/control-points/${queryArg.cpId}/destination-in-range`,
        params: { lat: queryArg.lat, lng: queryArg.lng },
      }),
    }),
    setControlPointDestination: build.mutation<
      SetControlPointDestinationApiResponse,
      SetControlPointDestinationApiArg
    >({
      query: (queryArg) => ({
        url: `/control-points/${queryArg.cpId}/destination`,
        method: "PUT",
        body: queryArg.body,
      }),
    }),
    clearControlPointDestination: build.mutation<
      ClearControlPointDestinationApiResponse,
      ClearControlPointDestinationApiArg
    >({
      query: (queryArg) => ({
        url: `/control-points/${queryArg.cpId}/cancel-travel`,
        method: "PUT",
      }),
    }),
    getDebugHoldZones: build.query<
      GetDebugHoldZonesApiResponse,
      GetDebugHoldZonesApiArg
    >({
      query: (queryArg) => ({
        url: `/debug/waypoint-geometries/hold/${queryArg.flightId}`,
      }),
    }),
    getDebugIpZones: build.query<
      GetDebugIpZonesApiResponse,
      GetDebugIpZonesApiArg
    >({
      query: (queryArg) => ({
        url: `/debug/waypoint-geometries/ip/${queryArg.flightId}`,
      }),
    }),
    getDebugJoinZones: build.query<
      GetDebugJoinZonesApiResponse,
      GetDebugJoinZonesApiArg
    >({
      query: (queryArg) => ({
        url: `/debug/waypoint-geometries/join/${queryArg.flightId}`,
      }),
    }),
    listFlights: build.query<ListFlightsApiResponse, ListFlightsApiArg>({
      query: (queryArg) => ({
        url: `/flights/`,
        params: { with_waypoints: queryArg.withWaypoints },
      }),
    }),
    getFlightById: build.query<GetFlightByIdApiResponse, GetFlightByIdApiArg>({
      query: (queryArg) => ({
        url: `/flights/${queryArg.flightId}`,
        params: { with_waypoints: queryArg.withWaypoints },
      }),
    }),
    getCommitBoundaryForFlight: build.query<
      GetCommitBoundaryForFlightApiResponse,
      GetCommitBoundaryForFlightApiArg
    >({
      query: (queryArg) => ({
        url: `/flights/${queryArg.flightId}/commit-boundary`,
      }),
    }),
    listFrontLines: build.query<
      ListFrontLinesApiResponse,
      ListFrontLinesApiArg
    >({
      query: () => ({ url: `/front-lines/` }),
    }),
    getFrontLineById: build.query<
      GetFrontLineByIdApiResponse,
      GetFrontLineByIdApiArg
    >({
      query: (queryArg) => ({ url: `/front-lines/${queryArg.frontLineId}` }),
    }),
    getGameState: build.query<GetGameStateApiResponse, GetGameStateApiArg>({
      query: () => ({ url: `/game/` }),
    }),
    getTerrainZones: build.query<
      GetTerrainZonesApiResponse,
      GetTerrainZonesApiArg
    >({
      query: () => ({ url: `/map-zones/terrain` }),
    }),
    listUnculledZones: build.query<
      ListUnculledZonesApiResponse,
      ListUnculledZonesApiArg
    >({
      query: () => ({ url: `/map-zones/unculled` }),
    }),
    getThreatZones: build.query<
      GetThreatZonesApiResponse,
      GetThreatZonesApiArg
    >({
      query: () => ({ url: `/map-zones/threats` }),
    }),
    getNavmesh: build.query<GetNavmeshApiResponse, GetNavmeshApiArg>({
      query: (queryArg) => ({
        url: `/navmesh/`,
        params: { for_player: queryArg.forPlayer },
      }),
    }),
    openNewFrontLinePackageDialog: build.mutation<
      OpenNewFrontLinePackageDialogApiResponse,
      OpenNewFrontLinePackageDialogApiArg
    >({
      query: (queryArg) => ({
        url: `/qt/create-package/front-line/${queryArg.frontLineId}`,
        method: "POST",
      }),
    }),
    openNewTgoPackageDialog: build.mutation<
      OpenNewTgoPackageDialogApiResponse,
      OpenNewTgoPackageDialogApiArg
    >({
      query: (queryArg) => ({
        url: `/qt/create-package/tgo/${queryArg.tgoId}`,
        method: "POST",
      }),
    }),
    openTgoInfoDialog: build.mutation<
      OpenTgoInfoDialogApiResponse,
      OpenTgoInfoDialogApiArg
    >({
      query: (queryArg) => ({
        url: `/qt/info/tgo/${queryArg.tgoId}`,
        method: "POST",
      }),
    }),
    openNewControlPointPackageDialog: build.mutation<
      OpenNewControlPointPackageDialogApiResponse,
      OpenNewControlPointPackageDialogApiArg
    >({
      query: (queryArg) => ({
        url: `/qt/create-package/control-point/${queryArg.cpId}`,
        method: "POST",
      }),
    }),
    openControlPointInfoDialog: build.mutation<
      OpenControlPointInfoDialogApiResponse,
      OpenControlPointInfoDialogApiArg
    >({
      query: (queryArg) => ({
        url: `/qt/info/control-point/${queryArg.cpId}`,
        method: "POST",
      }),
    }),
    listSupplyRoutes: build.query<
      ListSupplyRoutesApiResponse,
      ListSupplyRoutesApiArg
    >({
      query: () => ({ url: `/supply-routes/` }),
    }),
    listTgos: build.query<ListTgosApiResponse, ListTgosApiArg>({
      query: () => ({ url: `/tgos/` }),
    }),
    getTgoById: build.query<GetTgoByIdApiResponse, GetTgoByIdApiArg>({
      query: (queryArg) => ({ url: `/tgos/${queryArg.tgoId}` }),
    }),
    listAllWaypointsForFlight: build.query<
      ListAllWaypointsForFlightApiResponse,
      ListAllWaypointsForFlightApiArg
    >({
      query: (queryArg) => ({ url: `/waypoints/${queryArg.flightId}` }),
    }),
    setWaypointPosition: build.mutation<
      SetWaypointPositionApiResponse,
      SetWaypointPositionApiArg
    >({
      query: (queryArg) => ({
        url: `/waypoints/${queryArg.flightId}/${queryArg.waypointIdx}/position`,
        method: "POST",
        body: queryArg.leafletPoint,
      }),
    }),
    getIadsNetwork: build.query<
      GetIadsNetworkApiResponse,
      GetIadsNetworkApiArg
    >({
      query: () => ({ url: `/iads-network/` }),
    }),
    getIadsConnectionsForTgo: build.query<
      GetIadsConnectionsForTgoApiResponse,
      GetIadsConnectionsForTgoApiArg
    >({
      query: (queryArg) => ({ url: `/iads-network/for-tgo/${queryArg.tgoId}` }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as _liberationApi };
export type ListControlPointsApiResponse =
  /** status 200 Successful Response */ ControlPoint[];
export type ListControlPointsApiArg = void;
export type GetControlPointByIdApiResponse =
  /** status 200 Successful Response */ ControlPoint;
export type GetControlPointByIdApiArg = {
  cpId: string;
};
export type ControlPointDestinationInRangeApiResponse =
  /** status 200 Successful Response */ boolean;
export type ControlPointDestinationInRangeApiArg = {
  cpId: string;
  lat: number;
  lng: number;
};
export type SetControlPointDestinationApiResponse =
  /** status 204 Successful Response */ undefined;
export type SetControlPointDestinationApiArg = {
  cpId: string;
  body: LatLng;
};
export type ClearControlPointDestinationApiResponse =
  /** status 204 Successful Response */ undefined;
export type ClearControlPointDestinationApiArg = {
  cpId: string;
};
export type GetDebugHoldZonesApiResponse =
  /** status 200 Successful Response */ HoldZones;
export type GetDebugHoldZonesApiArg = {
  flightId: string;
};
export type GetDebugIpZonesApiResponse =
  /** status 200 Successful Response */ IpZones;
export type GetDebugIpZonesApiArg = {
  flightId: string;
};
export type GetDebugJoinZonesApiResponse =
  /** status 200 Successful Response */ JoinZones;
export type GetDebugJoinZonesApiArg = {
  flightId: string;
};
export type ListFlightsApiResponse =
  /** status 200 Successful Response */ Flight[];
export type ListFlightsApiArg = {
  withWaypoints?: boolean;
};
export type GetFlightByIdApiResponse =
  /** status 200 Successful Response */ Flight;
export type GetFlightByIdApiArg = {
  flightId: string;
  withWaypoints?: boolean;
};
export type GetCommitBoundaryForFlightApiResponse =
  /** status 200 Successful Response */ LatLng[][];
export type GetCommitBoundaryForFlightApiArg = {
  flightId: string;
};
export type ListFrontLinesApiResponse =
  /** status 200 Successful Response */ FrontLine[];
export type ListFrontLinesApiArg = void;
export type GetFrontLineByIdApiResponse =
  /** status 200 Successful Response */ FrontLine;
export type GetFrontLineByIdApiArg = {
  frontLineId: string;
};
export type GetGameStateApiResponse =
  /** status 200 Successful Response */ Game;
export type GetGameStateApiArg = void;
export type GetTerrainZonesApiResponse =
  /** status 200 Successful Response */ MapZones;
export type GetTerrainZonesApiArg = void;
export type ListUnculledZonesApiResponse =
  /** status 200 Successful Response */ UnculledZone[];
export type ListUnculledZonesApiArg = void;
export type GetThreatZonesApiResponse =
  /** status 200 Successful Response */ ThreatZoneContainer;
export type GetThreatZonesApiArg = void;
export type GetNavmeshApiResponse =
  /** status 200 Successful Response */ NavMesh;
export type GetNavmeshApiArg = {
  forPlayer: boolean;
};
export type OpenNewFrontLinePackageDialogApiResponse =
  /** status 200 Successful Response */ any;
export type OpenNewFrontLinePackageDialogApiArg = {
  frontLineId: string;
};
export type OpenNewTgoPackageDialogApiResponse =
  /** status 200 Successful Response */ any;
export type OpenNewTgoPackageDialogApiArg = {
  tgoId: string;
};
export type OpenTgoInfoDialogApiResponse =
  /** status 200 Successful Response */ any;
export type OpenTgoInfoDialogApiArg = {
  tgoId: string;
};
export type OpenNewControlPointPackageDialogApiResponse =
  /** status 200 Successful Response */ any;
export type OpenNewControlPointPackageDialogApiArg = {
  cpId: string;
};
export type OpenControlPointInfoDialogApiResponse =
  /** status 200 Successful Response */ any;
export type OpenControlPointInfoDialogApiArg = {
  cpId: string;
};
export type ListSupplyRoutesApiResponse =
  /** status 200 Successful Response */ SupplyRoute[];
export type ListSupplyRoutesApiArg = void;
export type ListTgosApiResponse = /** status 200 Successful Response */ Tgo[];
export type ListTgosApiArg = void;
export type GetTgoByIdApiResponse = /** status 200 Successful Response */ Tgo;
export type GetTgoByIdApiArg = {
  tgoId: string;
};
export type ListAllWaypointsForFlightApiResponse =
  /** status 200 Successful Response */ Waypoint[];
export type ListAllWaypointsForFlightApiArg = {
  flightId: string;
};
export type SetWaypointPositionApiResponse =
  /** status 204 Successful Response */ undefined;
export type SetWaypointPositionApiArg = {
  flightId: string;
  waypointIdx: number;
  leafletPoint: LatLng;
};
export type GetIadsNetworkApiResponse =
  /** status 200 Successful Response */ IadsNetwork;
export type GetIadsNetworkApiArg = void;
export type GetIadsConnectionsForTgoApiResponse =
  /** status 200 Successful Response */ IadsConnection[];
export type GetIadsConnectionsForTgoApiArg = {
  tgoId: string;
};
export type LatLng = {
  lat: number;
  lng: number;
};
export type ControlPoint = {
  id: string;
  name: string;
  blue: boolean;
  position: LatLng;
  mobile: boolean;
  destination?: LatLng;
  sidc: string;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type HoldZones = {
  homeBubble: LatLng[][];
  targetBubble: LatLng[][];
  joinBubble: LatLng[][];
  excludedZones: LatLng[][][];
  permissibleZones: LatLng[][][];
  preferredLines: LatLng[][];
};
export type IpZones = {
  homeBubble: LatLng[][];
  ipBubble: LatLng[][];
  permissibleZone: LatLng[][];
  safeZones: LatLng[][][];
};
export type JoinZones = {
  homeBubble: LatLng[][];
  targetBubble: LatLng[][];
  ipBubble: LatLng[][];
  excludedZones: LatLng[][][];
  permissibleZones: LatLng[][][];
  preferredLines: LatLng[][];
};
export type Waypoint = {
  name: string;
  position: LatLng;
  altitude_ft: number;
  altitude_reference: string;
  is_movable: boolean;
  should_mark: boolean;
  include_in_path: boolean;
  timing: string;
};
export type Flight = {
  id: string;
  blue: boolean;
  position?: LatLng;
  sidc: string;
  waypoints?: Waypoint[];
};
export type FrontLine = {
  id: string;
  extents: LatLng[];
};
export type Tgo = {
  id: string;
  name: string;
  control_point_name: string;
  category: string;
  blue: boolean;
  position: LatLng;
  units: string[];
  threat_ranges: number[];
  detection_ranges: number[];
  dead: boolean;
  sidc: string;
};
export type SupplyRoute = {
  id: string;
  points: LatLng[];
  front_active: boolean;
  is_sea: boolean;
  blue: boolean;
  active_transports: string[];
};
export type IadsConnection = {
  id: string;
  points: LatLng[];
  node: string;
  connected: string;
  active: boolean;
  blue: boolean;
  is_power: boolean;
};
export type IadsNetwork = {
  advanced: boolean;
  connections: IadsConnection[];
};
export type ThreatZones = {
  full: LatLng[][][];
  aircraft: LatLng[][][];
  air_defenses: LatLng[][][];
  radar_sams: LatLng[][][];
};
export type ThreatZoneContainer = {
  blue: ThreatZones;
  red: ThreatZones;
};
export type NavMeshPoly = {
  poly: LatLng[][];
  threatened: boolean;
};
export type NavMesh = {
  polys: NavMeshPoly[];
};
export type NavMeshes = {
  blue: NavMesh;
  red: NavMesh;
};
export type UnculledZone = {
  position: LatLng;
  radius: number;
};
export type Game = {
  control_points: ControlPoint[];
  tgos: Tgo[];
  supply_routes: SupplyRoute[];
  front_lines: FrontLine[];
  flights: Flight[];
  iads_network: IadsNetwork;
  threat_zones: ThreatZoneContainer;
  navmeshes: NavMeshes;
  map_center?: LatLng;
  unculled_zones: UnculledZone[];
};
export type MapZones = {
  inclusion: LatLng[][][];
  exclusion: LatLng[][][];
  sea: LatLng[][][];
};
export const {
  useListControlPointsQuery,
  useGetControlPointByIdQuery,
  useControlPointDestinationInRangeQuery,
  useSetControlPointDestinationMutation,
  useClearControlPointDestinationMutation,
  useGetDebugHoldZonesQuery,
  useGetDebugIpZonesQuery,
  useGetDebugJoinZonesQuery,
  useListFlightsQuery,
  useGetFlightByIdQuery,
  useGetCommitBoundaryForFlightQuery,
  useListFrontLinesQuery,
  useGetFrontLineByIdQuery,
  useGetGameStateQuery,
  useGetTerrainZonesQuery,
  useListUnculledZonesQuery,
  useGetThreatZonesQuery,
  useGetNavmeshQuery,
  useOpenNewFrontLinePackageDialogMutation,
  useOpenNewTgoPackageDialogMutation,
  useOpenTgoInfoDialogMutation,
  useOpenNewControlPointPackageDialogMutation,
  useOpenControlPointInfoDialogMutation,
  useListSupplyRoutesQuery,
  useListTgosQuery,
  useGetTgoByIdQuery,
  useListAllWaypointsForFlightQuery,
  useSetWaypointPositionMutation,
  useGetIadsNetworkQuery,
  useGetIadsConnectionsForTgoQuery,
} = injectedRtkApi;
