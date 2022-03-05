import { selectFlights } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import Aircraft from "../aircraft";
import { LayerGroup } from "react-leaflet";

export default function AircraftLayer() {
  const atos = useAppSelector(selectFlights);
  return (
    <LayerGroup>
      {Object.values(atos.blue).map((flight) => {
        return <Aircraft key={flight.id} flight={flight} />;
      })}
      {Object.values(atos.red).map((flight) => {
        return <Aircraft key={flight.id} flight={flight} />;
      })}
    </LayerGroup>
  );
}
