import { selectNavMeshes } from "../../api/navMeshSlice";
import { useAppSelector } from "../../app/hooks";
import { LayerGroup, Polygon } from "react-leaflet";

interface NavMeshLayerProps {
  blue: boolean;
}

export default function NavMeshLayer(props: NavMeshLayerProps) {
  const meshes = useAppSelector(selectNavMeshes);
  const mesh = props.blue ? meshes.blue : meshes.red;
  return (
    <LayerGroup>
      {mesh.map((zone, idx) => {
        return (
          <Polygon
            key={idx}
            positions={zone.poly}
            color="#000000"
            weight={1}
            fill
            fillColor={zone.threatened ? "#ff0000" : "#00ff00"}
            fillOpacity={0.1}
            noClip
            interactive={false}
          />
        );
      })}
    </LayerGroup>
  );
}
