import { useGetDebugIpZonesQuery } from "../../api/liberationApi";
import { LayerGroup, Polygon } from "react-leaflet";

interface IpZonesProps {
  flightId: string;
}

function IpZones(props: IpZonesProps) {
  const { data, error, isLoading } = useGetDebugIpZonesQuery({
    flightId: props.flightId,
  });

  if (isLoading) {
    return <></>;
  }

  if (error) {
    console.error("Error while loading waypoint IP zone info", error);
    return <></>;
  }

  if (!data) {
    console.log("Waypoint IP zone returned empty response");
    return <></>;
  }

  return (
    <>
      <Polygon
        positions={data.homeBubble}
        color="#ffff00"
        fillOpacity={0.1}
        interactive={false}
      />
      <Polygon
        positions={data.ipBubble}
        color="#bb89ff"
        fillOpacity={0.1}
        interactive={false}
      />
      <Polygon
        positions={data.permissibleZone}
        color="#ffffff"
        fillOpacity={0.1}
        interactive={false}
      />

      {data.safeZones.map((zone, idx) => {
        return (
          <Polygon
            key={idx}
            positions={zone}
            color="#80BA80"
            fillOpacity={0.1}
            interactive={false}
          />
        );
      })}
    </>
  );
}

interface IpZonesLayerProps {
  flightId: string | null;
}

export function IpZonesLayer(props: IpZonesLayerProps) {
  return (
    <LayerGroup>
      {props.flightId ? <IpZones flightId={props.flightId} /> : <></>}
    </LayerGroup>
  );
}
