import { LayerGroup } from "react-leaflet";
import { useAppSelector } from "../../app/hooks";
import { selectControlPoints } from "../../game/theater/theaterSlice";
import { ControlPoint } from "../controlpoint/ControlPoint";

export function ControlPointsLayer() {
  const controlPoints = useAppSelector(selectControlPoints);
  console.log(`controlPoints is ${controlPoints}`);
  return (
    <LayerGroup>
      {controlPoints.map((controlPoint) => {
        return (
          <ControlPoint key={controlPoint.name} controlPoint={controlPoint} />
        );
      })}
    </LayerGroup>
  );
}
