import { Icon, Point } from "leaflet";
import { Marker, Popup } from "react-leaflet";

import { Symbol as MilSymbol } from "milsymbol";
import { Tgo as TgoModel } from "../../api/tgo";

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
      <Popup>
        {`${props.tgo.name} (${props.tgo.control_point_name})`}
        <br />
        {props.tgo.units.map((unit) => (
          <>
            {unit}
            <br />
          </>
        ))}
      </Popup>
    </Marker>
  );
}
