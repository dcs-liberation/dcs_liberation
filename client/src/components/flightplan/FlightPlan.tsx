import { Flight } from "../../api/flight";
import { Polyline } from "react-leaflet";

const BLUE_PATH = "#0084ff";
const RED_PATH = "#c85050";

interface FlightPlanProps {
  flight: Flight;
  selected: boolean;
}

function FlightPlanPath(props: FlightPlanProps) {
  const color = props.flight.blue ? BLUE_PATH : RED_PATH;
  const waypoints = props.flight.waypoints;
  if (waypoints == null) {
    return <></>;
  }
  const points = waypoints.map((waypoint) => waypoint.position);
  return (
    <Polyline
      positions={points}
      pathOptions={{ color: color, interactive: false }}
    />
  );
}

export default function FlightPlan(props: FlightPlanProps) {
  return (
    <>
      <FlightPlanPath {...props} />
    </>
  );
}
