import { Tgo } from "../../api/liberationApi";
import { selectTgos } from "../../api/tgosSlice";
import { useAppSelector } from "../../app/hooks";
import { Circle, LayerGroup } from "react-leaflet";

interface TgoRangeCirclesProps {
  tgo: Tgo;
  blue: boolean;
  detection?: boolean;
}

function colorFor(blue: boolean, detection: boolean) {
  if (blue) {
    return detection ? "#bb89ff" : "#0084ff";
  }
  return detection ? "#eee17b" : "#c85050";
}

const TgoRangeCircles = (props: TgoRangeCirclesProps) => {
  const radii = props.detection
    ? props.tgo.detection_ranges
    : props.tgo.threat_ranges;
  const color = colorFor(props.blue, props.detection === true);
  const weight = props.detection ? 1 : 2;

  return (
    <>
      {radii.map((radius, idx) => {
        return (
          <Circle
            key={idx}
            center={props.tgo.position}
            radius={radius}
            color={color}
            fill={false}
            weight={weight}
            interactive={false}
          />
        );
      })}
    </>
  );
};

interface AirDefenseRangeLayerProps {
  blue: boolean;
  detection?: boolean;
}

export const AirDefenseRangeLayer = (props: AirDefenseRangeLayerProps) => {
  const tgos = Object.values(useAppSelector(selectTgos).tgos);
  var tgosForSide = tgos.filter((tgo) => tgo.blue === props.blue);

  return (
    <LayerGroup>
      {tgosForSide.map((tgo) => {
        return (
          <TgoRangeCircles key={tgo.id} tgo={tgo} {...props}></TgoRangeCircles>
        );
      })}
    </LayerGroup>
  );
};

export default AirDefenseRangeLayer;
