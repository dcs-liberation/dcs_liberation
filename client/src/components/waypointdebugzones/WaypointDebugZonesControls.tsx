import { selectSelectedFlightId } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import { HoldZonesLayer } from "./HoldZones";
import { JoinZonesLayer } from "./JoinZones";
import { LayersControl } from "react-leaflet";

const ENABLE_EXPENSIVE_DEBUG_TOOLS = false;

export function WaypointDebugZonesControls() {
  const selectedFlightId = useAppSelector(selectSelectedFlightId);

  if (!ENABLE_EXPENSIVE_DEBUG_TOOLS) {
    return <></>;
  }

  return (
    <>
      <LayersControl.Overlay name="Join zones">
        <JoinZonesLayer flightId={selectedFlightId} />
      </LayersControl.Overlay>
      <LayersControl.Overlay name="Hold zones">
        <HoldZonesLayer flightId={selectedFlightId} />
      </LayersControl.Overlay>
    </>
  );
}
