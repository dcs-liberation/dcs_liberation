import { useListUnculledZonesQuery, UnculledZone } from "../../api/liberationApi";
import { LayerGroup, LayersControl, Circle } from "react-leaflet";

interface CullingExclusionCirclesProps {
  zones: UnculledZone[];
}

const CullingExclusionCircles = (props: CullingExclusionCirclesProps) => {
  return (
    <>
      <LayerGroup>
        {props.zones.map((zone, idx) => {
          return (
            <Circle
              key={idx}
              center={zone.position}
              radius={zone.radius}
              color="#b4ff8c"
              fill={false}
              interactive={false}
            />
          );
        })}
      </LayerGroup>
    </>
  );
};

export default function CullingExclusionZones() {
  const { data, error, isLoading } = useListUnculledZonesQuery();
  var cez = <></>;

  if (error) {
    console.error("Error while loading terrain zones", error);
  } else if (isLoading) {
  } else if (!data) {
    console.log("Empty response when loading terrain zones");
  } else {
    cez = (
      <CullingExclusionCircles zones={data}></CullingExclusionCircles>
    );
  }
  return (
    <LayersControl.Overlay name="Culling exclusion zones">
      {cez}
    </LayersControl.Overlay>
  );
}
