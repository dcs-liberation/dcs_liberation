import { Marker, Tooltip, useMap, useMapEvent } from "react-leaflet";
import { MutableRefObject, useCallback, useEffect, useRef } from "react";

import { Icon } from "leaflet";
import { Marker as LMarker } from "leaflet";
import { Waypoint } from "../../api/waypoint";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

const WAYPOINT_ICON = new Icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
});

interface WaypointMarkerProps {
  number: number;
  waypoint: Waypoint;
}

const WaypointMarker = (props: WaypointMarkerProps) => {
  // Most props of react-leaflet types are immutable and components will not
  // update to account for changes, so we can't simply use the `permanent`
  // property of the tooltip to control tooltip visibility based on the zoom
  // level.
  //
  // On top of that, listening for zoom changes and opening/closing is not
  // sufficient because clicking anywhere will close any opened tooltips (even
  // if they are permanent; once openTooltip has been called that seems to no
  // longer have any effect).
  //
  // Instead, listen for zoom changes and rebind the tooltip when the zoom level
  // changes.
  const map = useMap();
  const marker: MutableRefObject<LMarker | undefined> = useRef();

  const rebindTooltip = useCallback(() => {
    if (marker.current === undefined) {
      return;
    }

    const tooltip = marker.current.getTooltip();
    if (tooltip === undefined) {
      return;
    }

    const permanent = map.getZoom() >= 9;
    marker.current
      .unbindTooltip()
      .bindTooltip(tooltip, { permanent: permanent });
  }, [map]);
  useMapEvent("zoomend", rebindTooltip);

  const waypoint = props.waypoint;
  return (
    <Marker
      position={waypoint.position}
      icon={WAYPOINT_ICON}
      ref={(ref) => {
        if (ref != null) {
          marker.current = ref;
        }
      }}
    >
      <Tooltip position={waypoint.position}>
        {`${props.number} ${waypoint.name}`}
        <br />
        {`${waypoint.altitude_ft} ft ${waypoint.altitude_reference}`}
        <br />
        TODO: Timing info
      </Tooltip>
    </Marker>
  );
};

export default WaypointMarker;
