import FlightPlan from "../flightplan";
import { LayerGroup } from "react-leaflet";
import { selectFlights } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";

interface FlightPlansLayerProps {
  blue: boolean;
}

export default function FlightPlansLayer(props: FlightPlansLayerProps) {
  const atos = useAppSelector(selectFlights);
  const flights = props.blue ? atos.blue : atos.red;
  return (
    <LayerGroup>
      {Object.values(flights).map((flight) => {
        return <FlightPlan key={flight.id} flight={flight} selected={false} />;
      })}
    </LayerGroup>
  );
}
