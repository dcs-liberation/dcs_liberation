import { LayerGroup } from "react-leaflet";
import Tgo from "../tgos/Tgo";
import { TgoType } from "../../api/tgo";
import { selectTgos } from "../../api/tgosSlice";
import { useAppSelector } from "../../app/hooks";

interface TgosLayerProps {
  type: TgoType;
}

export default function TgosLayer(props: TgosLayerProps) {
  const allTgos = useAppSelector(selectTgos);
  const tgos = allTgos.tgosByType[props.type];
  console.dir(Object.entries(TgoType));
  return (
    <LayerGroup>
      {tgos.map((tgo) => {
        return <Tgo key={tgo.name} tgo={tgo} />;
      })}
    </LayerGroup>
  );
}
