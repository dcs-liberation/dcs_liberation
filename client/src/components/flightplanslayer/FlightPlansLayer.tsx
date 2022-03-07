import { Flight } from "../../api/flight";
import { selectFlights, selectSelectedFlight } from "../../api/flightsSlice";
import { useAppSelector } from "../../app/hooks";
import FlightPlan from "../flightplan";
import { LayerGroup } from "react-leaflet";

interface FlightPlansLayerProps {
  blue: boolean;
}

function SelectedFlightPlan(props: FlightPlansLayerProps) {
  const flight = useAppSelector(selectSelectedFlight);
  if (!flight) {
    return <></>;
  }

  if (!props.blue) {
    // We don't currently support playing as red, so nothing to draw.
    return <></>;
  }

  return <FlightPlan key={flight.id} flight={flight} selected={true} />;
}

export default function FlightPlansLayer(props: FlightPlansLayerProps) {
  const flightData = useAppSelector(selectFlights);
  const isNotSelected = (flight: Flight) => {
    if (flightData.selected == null) {
      return true;
    }
    return flightData.selected !== flight.id;
  };

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
      <SelectedFlightPlan {...props} />
    </LayerGroup>
  );
}
