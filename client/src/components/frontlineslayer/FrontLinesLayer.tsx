import FrontLine from "../frontline";
import { LayerGroup } from "react-leaflet";
import { selectFrontLines } from "../../api/frontLinesSlice";
import { useAppSelector } from "../../app/hooks";

export default function SupplyRoutesLayer() {
  const fronts = useAppSelector(selectFrontLines).fronts;
  return (
    <LayerGroup>
      {fronts.map((front, idx) => {
        return <FrontLine key={idx} front={front} />;
      })}
    </LayerGroup>
  );
}
