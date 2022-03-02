import { Flight } from "../../api/flight";
import { Polyline } from "react-leaflet";

const BLUE_PATH = "#0084ff";
const RED_PATH = "#c85050";
const SELECTED_PATH = "#ffff00";

interface FlightPlanProps {
  flight: Flight;
  selected: boolean;
}

const pathColor = (props: FlightPlanProps) => {
  if (props.selected) {
    return SELECTED_PATH;
  } else if (props.flight.blue) {
    return BLUE_PATH;
  } else {
    return RED_PATH;
  }
};

function FlightPlanPath(props: FlightPlanProps) {
  const color = pathColor(props);
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
