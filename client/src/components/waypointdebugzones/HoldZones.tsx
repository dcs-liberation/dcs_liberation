import { useGetDebugHoldZonesQuery } from "../../api/liberationApi";
import { LayerGroup, Polygon, Polyline } from "react-leaflet";

interface HoldZonesProps {
  flightId: string;
}

function HoldZones(props: HoldZonesProps) {
  const { data, error, isLoading } = useGetDebugHoldZonesQuery({
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
        positions={data.targetBubble}
        color="#ffff00"
        fillOpacity={0.1}
        interactive={false}
      />
      <Polygon
        positions={data.joinBubble}
        color="#ffff00"
        fillOpacity={0.1}
        interactive={false}
      />

      {data.excludedZones.map((zone, idx) => {
        return (
          <Polygon
            key={idx}
            positions={zone}
            color="#ffa500"
            stroke={false}
            fillOpacity={0.2}
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

interface HoldZonesLayerProps {
  flightId: string | null;
}

export function HoldZonesLayer(props: HoldZonesLayerProps) {
  return (
    <LayerGroup>
      {props.flightId ? <HoldZones flightId={props.flightId} /> : <></>}
    </LayerGroup>
  );
}
