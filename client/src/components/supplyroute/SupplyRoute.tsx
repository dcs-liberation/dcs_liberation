import { SupplyRoute as SupplyRouteModel } from "../../api/liberationApi";
import SplitLines from "../splitlines/SplitLines";
import { Polyline as LPolyline } from "leaflet";
import { useEffect, useRef } from "react";
import { Polyline, Tooltip } from "react-leaflet";

interface SupplyRouteProps {
  route: SupplyRouteModel;
}

function SupplyRouteTooltip(props: SupplyRouteProps) {
  if (!props.route.active_transports.length) {
    return <Tooltip>This supply route is inactive.</Tooltip>;
  }

  return (
    <Tooltip>
      <SplitLines items={props.route.active_transports} />
    </Tooltip>
  );
}

function ActiveSupplyRouteHighlight(props: SupplyRouteProps) {
  if (!props.route.active_transports.length) {
    return <></>;
  }

  return (
    <Polyline positions={props.route.points} color={"#ffffff"} weight={2} />
  );
}

function colorFor(route: SupplyRouteModel) {
  if (route.front_active) {
    return "#c85050";
  }
  if (route.blue) {
    return "#2d3e50";
  }
  return "#8c1414";
}

export default function SupplyRoute(props: SupplyRouteProps) {
  const color = colorFor(props.route);
  const weight = props.route.is_sea ? 4 : 6;

  const path = useRef<LPolyline | null>();

  useEffect(() => {
    // Ensure that the highlight line draws on top of this. We have to bring
    // this to the back rather than bringing the highlight to the front because
    // the highlight won't necessarily be drawn yet.
    path.current?.bringToBack();
  });

  return (
    <Polyline
      positions={props.route.points}
      color={color}
      weight={weight}
      ref={(ref) => (path.current = ref)}
    >
      <SupplyRouteTooltip {...props} />
      <ActiveSupplyRouteHighlight {...props} />
    </Polyline>
  );
}
