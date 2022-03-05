import { Flight } from "../../api/flight";
import { selectFlights } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import FlightPlan from "../flightplan";
import { LayerGroup } from "react-leaflet";

interface FlightPlansLayerProps {
  blue: boolean;
}

export default function FlightPlansLayer(props: FlightPlansLayerProps) {
  const flightData = useAppSelector(selectFlights);
  const isNotSelected = (flight: Flight) => {
    if (flightData.selected == null) {
      return true;
    }
    return flightData.selected.id !== flight.id;
  };

  const selectedFlight =
    flightData.selected && flightData.selected.blue === props.blue ? (
      <FlightPlan
        key={flightData.selected.id}
        flight={flightData.selected}
        selected={true}
      />
    ) : (
      <></>
    );

  return (
    <LayerGroup>
      {Object.values(flightData.flights)
        .filter(isNotSelected)
        .filter((flight) => props.blue === flight.blue)
        .map((flight) => {
          return (
            <FlightPlan key={flight.id} flight={flight} selected={false} />
          );
        })}
      {selectedFlight}
    </LayerGroup>
  );
}
