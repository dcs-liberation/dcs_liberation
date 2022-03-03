import { LayerGroup } from "react-leaflet";
import SupplyRoute from "../supplyroute/SupplyRoute";
import { selectSupplyRoutes } from "../../api/supplyRoutesSlice";
import { useAppSelector } from "../../app/hooks";

export default function SupplyRoutesLayer() {
  const routes = useAppSelector(selectSupplyRoutes).routes;
  return (
    <LayerGroup>
      {routes.map((route, idx) => {
        return <SupplyRoute key={idx} route={route} />;
      })}
    </LayerGroup>
  );
}
