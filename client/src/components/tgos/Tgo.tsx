import { Tgo as TgoModel } from "../../api/tgo";
import SplitLines from "../splitlines/SplitLines";
import { Icon, Point } from "leaflet";
import { Symbol as MilSymbol } from "milsymbol";
import { Marker, Tooltip } from "react-leaflet";

function iconForTgo(cp: TgoModel) {
  const symbol = new MilSymbol(cp.sidc, {
    size: 24,
  });

  return new Icon({
    iconUrl: symbol.toDataURL(),
    iconAnchor: new Point(symbol.getAnchor().x, symbol.getAnchor().y),
  });
}

interface TgoProps {
  tgo: TgoModel;
}

export default function Tgo(props: TgoProps) {
  return (
    <Marker position={props.tgo.position} icon={iconForTgo(props.tgo)}>
      <Tooltip>
        {`${props.tgo.name} (${props.tgo.control_point_name})`}
        <br />
        <SplitLines items={props.tgo.units} />
      </Tooltip>
    </Marker>
  );
}
