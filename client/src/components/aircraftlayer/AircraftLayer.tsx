import { selectFlights } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import Aircraft from "../aircraft";
import { LayerGroup } from "react-leaflet";

export default function AircraftLayer() {
  const flights = useAppSelector(selectFlights).flights;
  return (
    <LayerGroup>
      {Object.values(flights).map((flight) => {
        return <Aircraft key={flight.id} flight={flight} />;
      })}
    </LayerGroup>
  );
}
