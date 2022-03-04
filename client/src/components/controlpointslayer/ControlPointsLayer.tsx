import ControlPoint from "../controlpoints";
import { LayerGroup } from "react-leaflet";
import { selectControlPoints } from "../../api/controlPointsSlice";
import { useAppSelector } from "../../app/hooks";

export default function ControlPointsLayer() {
  const controlPoints = useAppSelector(selectControlPoints);
  return (
    <LayerGroup>
      {Object.values(controlPoints.controlPoints).map((controlPoint) => {
        return (
          <ControlPoint key={controlPoint.name} controlPoint={controlPoint} />
        );
      })}
    </LayerGroup>
  );
}
