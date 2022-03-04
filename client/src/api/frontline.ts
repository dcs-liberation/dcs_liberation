import { LatLng } from "leaflet";

export interface FrontLine {
  id: string;
  extents: LatLng[];
}

export default FrontLine;
