import { Flight } from "../../api/liberationApi";
import { useGetCommitBoundaryForFlightQuery } from "../../api/liberationApi";
import WaypointMarker from "../waypointmarker";
import { Polyline as LPolyline } from "leaflet";
import { ReactElement, useEffect, useRef } from "react";
import { Polyline } from "react-leaflet";

const BLUE_PATH = "#0084ff";
const RED_PATH = "#c85050";
const SELECTED_PATH = "#ffff00";

interface FlightPlanProps {
  flight: Flight;
  selected: boolean;
  highlight?: boolean;
}

const pathColor = (props: FlightPlanProps) => {
  if (props.selected && props.highlight) {
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

  const polylineRef = useRef<LPolyline | null>(null);

  // Flight paths should be drawn under everything else. There seems to be an
  // issue where `interactive: false` doesn't do as its told (there's nuance,
  // see the bug for details). It looks better if we draw the other elements on
  // top of the flight plans anyway, so just push the flight plan to the back.
  //
  // https://github.com/dcs-liberation/dcs_liberation/issues/3295
  //
  // It's not possible to z-index a polyline (and leaflet says it never will be,
  // because this is a limitation of SVG, not leaflet:
  // https://github.com/Leaflet/Leaflet/issues/185), so we need to use
  // bringToBack() to push the flight paths to the back of the drawing once
  // they've been added to the map. They'll still draw on top of the map, but
  // behind everything than was added before them. Anything added after always
  // goes on top.
  useEffect(() => {
    if (!props.selected) {
      polylineRef.current?.bringToBack();
    }
  });

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
      ref={polylineRef}
    />
  );
}

const WaypointMarkers = (props: FlightPlanProps) => {
  if (!props.selected || props.flight.waypoints == null) {
    return <></>;
  }

  var markers: ReactElement[] = [];
  props.flight.waypoints?.forEach((p, idx) => {
    if (p.should_mark) {
      markers.push(
        <WaypointMarker
          key={idx}
          number={idx}
          waypoint={p}
          flight={props.flight}
        />
      );
    }
  });

  return <>{markers}</>;
};

interface CommitBoundaryProps {
  flightId: string;
  selected: boolean;
}

function CommitBoundary(props: CommitBoundaryProps) {
  const { data, error, isLoading } = useGetCommitBoundaryForFlightQuery(
    {
      flightId: props.flightId,
    },
    // RTK Query doesn't seem to allow us to invalidate the cache from anything
    // but a mutation, but this data can be invalidated by events from the
    // websocket. Just disable the cache for this.
    //
    // This isn't perfect. It won't redraw until the component remounts. There
    // doesn't appear to be a better way.
    { refetchOnMountOrArgChange: true }
  );
  if (isLoading) {
    return <></>;
  }
  if (error) {
    console.error(`Error loading commit boundary for ${props.flightId}`, error);
    return <></>;
  }
  if (!data) {
    console.log(
      `Null response data when loading commit boundary for ${props.flightId}`
    );
    return <></>;
  }
  return (
    <Polyline positions={data} color="#ffff00" weight={1} interactive={false} />
  );
}

function CommitBoundaryIfSelected(props: CommitBoundaryProps) {
  if (!props.selected) {
    return <></>;
  }
  return <CommitBoundary {...props} />;
}

export default function FlightPlan(props: FlightPlanProps) {
  return (
    <>
      <FlightPlanPath {...props} />
      <WaypointMarkers {...props} />
      <CommitBoundaryIfSelected
        flightId={props.flight.id}
        selected={props.selected}
      />
    </>
  );
}
