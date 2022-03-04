import { Flight } from "../../api/flight";
import WaypointMarker from "../waypointmarker";
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
  const points = waypoints
    .filter((waypoint) => waypoint.include_in_path)
    .map((waypoint) => waypoint.position);
  return (
    <Polyline
      positions={points}
      pathOptions={{ color: color, interactive: false }}
    />
  );
}

const WaypointMarkers = (props: FlightPlanProps) => {
  if (!props.selected || props.flight.waypoints == null) {
    return <></>;
  }

  return (
    <>
      {props.flight.waypoints
        .filter((p) => p.should_mark)
        .map((p, idx) => {
          return (
            <WaypointMarker
              key={idx}
              number={idx}
              waypoint={p}
            ></WaypointMarker>
          );
        })}
    </>
  );
};

export default function FlightPlan(props: FlightPlanProps) {
  return (
    <>
      <FlightPlanPath {...props} />
      <WaypointMarkers {...props} />
    </>
  );
}
