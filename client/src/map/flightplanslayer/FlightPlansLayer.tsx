import { FlightPlan } from "../flightplan/FlightPlan";
import { LayerGroup } from "react-leaflet";
import { selectAtos } from "../../game/ato/atoSlice";
import { useAppSelector } from "../../app/hooks";

interface FlightPlansLayerProps {
  blue: boolean;
}

export function FlightPlansLayer(props: FlightPlansLayerProps) {
  const atos = useAppSelector(selectAtos);
  const flights = props.blue ? atos.blue : atos.red;
  return (
    <LayerGroup>
      {Object.values(flights).map((flight) => {
        return <FlightPlan key={flight.id} flight={flight} selected={false} />;
      })}
    </LayerGroup>
  );
}
