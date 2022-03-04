import { Flight } from "../../api/flight";
import { selectFlights } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import FlightPlan from "../flightplan";
import { LayerGroup } from "react-leaflet";

interface FlightPlansLayerProps {
  blue: boolean;
}

export default function FlightPlansLayer(props: FlightPlansLayerProps) {
  const atos = useAppSelector(selectFlights);
  const flights = props.blue ? atos.blue : atos.red;
  const isNotSelected = (flight: Flight) => {
    if (atos.selected == null) {
      return true;
    }
    return atos.selected.id !== flight.id;
  };

  const selectedFlight = atos.selected ? (
    <FlightPlan key={atos.selected.id} flight={atos.selected} selected={true} />
  ) : (
    <></>
  );

  return (
    <LayerGroup>
      {Object.values(flights)
        .filter(isNotSelected)
        .map((flight) => {
          return (
            <FlightPlan key={flight.id} flight={flight} selected={false} />
          );
        })}
      {selectedFlight}
    </LayerGroup>
  );
}
