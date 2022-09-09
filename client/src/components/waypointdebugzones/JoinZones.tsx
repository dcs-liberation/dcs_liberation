import { useGetDebugJoinZonesQuery } from "../../api/liberationApi";
import { LayerGroup, Polygon, Polyline } from "react-leaflet";

interface JoinZonesProps {
  flightId: string;
}

function JoinZones(props: JoinZonesProps) {
  const { data, error, isLoading } = useGetDebugJoinZonesQuery({
    flightId: props.flightId,
  });

  if (isLoading) {
    return <></>;
  }

  if (error) {
    console.error("Error while loading waypoint join zone info", error);
    return <></>;
  }

  if (!data) {
    console.log("Waypoint join zone returned empty response");
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
        positions={data.targetBubble}
        color="#bb89ff"
        fillOpacity={0.1}
        interactive={false}
      />
      <Polygon
        positions={data.ipBubble}
        color="#ffffff"
        fillOpacity={0.1}
        interactive={false}
      />

      {data.excludedZones.map((zone, idx) => {
        return (
          <Polygon
            key={idx}
            positions={zone}
            color="#ffa500"
            fillOpacity={0.2}
            stroke={false}
            interactive={false}
          />
        );
      })}

      {data.permissibleZones.map((zone, idx) => {
        return (
          <Polygon
            key={idx}
            positions={zone}
            color="#80BA80"
            interactive={false}
            stroke={false}
          />
        );
      })}

      {data.preferredLines.map((zone, idx) => {
        return (
          <Polyline
            key={idx}
            positions={zone}
            color="#80BA80"
            interactive={false}
          />
        );
      })}
    </>
  );
}

interface JoinZonesLayerProps {
  flightId: string | null;
}

export function JoinZonesLayer(props: JoinZonesLayerProps) {
  return (
    <LayerGroup>
      {props.flightId ? <JoinZones flightId={props.flightId} /> : <></>}
    </LayerGroup>
  );
}
