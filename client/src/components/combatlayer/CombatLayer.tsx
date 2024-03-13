import { selectCombat } from "../../api/combatSlice";
import { useAppSelector } from "../../app/hooks";
import Combat from "../combat/Combat";
import { LayerGroup } from "react-leaflet";

export default function CombatLayer() {
  const combats = useAppSelector(selectCombat);
  return (
    <LayerGroup>
      {Object.values(combats.combat).map((combat) => {
        return <Combat key={combat.id} combat={combat} />;
      })}
      (
    </LayerGroup>
  );
}
