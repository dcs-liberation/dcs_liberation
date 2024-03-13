import { selectTgos } from "../../api/tgosSlice";
import { useAppSelector } from "../../app/hooks";
import Tgo from "../tgos/Tgo";
import { LayerGroup } from "react-leaflet";

interface TgosLayerProps {
  categories?: string[];
  exclude?: true;
}

export default function TgosLayer(props: TgosLayerProps) {
  const allTgos = Object.values(useAppSelector(selectTgos).tgos);
  const categoryFilter = props.categories ?? [];
  const tgos = allTgos.filter(
    (tgo) => categoryFilter.includes(tgo.category) === !(props.exclude ?? false)
  );
  return (
    <LayerGroup>
      {tgos.map((tgo) => {
        return <Tgo key={tgo.name} tgo={tgo} />;
      })}
    </LayerGroup>
  );
}
