import { Flight } from "../../api/liberationApi";
import { Icon, Point } from "leaflet";
import { Symbol } from "milsymbol";
import { Marker } from "react-leaflet";

function iconForFlight(flight: Flight) {
  const symbol = new Symbol(flight.sidc, {
    size: 20,
  });

  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

interface AircraftProps {
  flight: Flight;
}

export default function Aircraft(props: AircraftProps) {
  if (!props.flight.position) {
    return <></>;
  }

  return (
    <Marker
      position={props.flight.position}
      icon={iconForFlight(props.flight)}
    />
  );
}
