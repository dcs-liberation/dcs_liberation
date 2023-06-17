import { selectFrontLines } from "../../api/frontLinesSlice";
import { useAppSelector } from "../../app/hooks";
import FrontLine from "../frontline";
import { LayerGroup } from "react-leaflet";

export default function FrontLinesLayer() {
  const fronts = useAppSelector(selectFrontLines).fronts;
  return (
    <LayerGroup>
      {Object.values(fronts).map((front, idx) => {
        return <FrontLine key={idx} front={front} />;
      })}
    </LayerGroup>
  );
}
