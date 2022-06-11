import { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet-ruler/src/leaflet-ruler.css";
import "leaflet-ruler";
import "./Ruler.css"

export default function LeafletRuler() {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    var options = {
          position: 'topleft',
          circleMarker: {               // Leaflet circle marker options for points used in this plugin
            color: 'yellow',
            radius: 2
          },
          lineStyle: {                  // Leaflet polyline options for lines used in this plugin
            color: 'yellow',
            dashArray: '1,6'
          },
          lengthUnit: {
            factor: 0.539956803,    //  from km to nm
            display: 'NM',
            decimal: 2,
            label: "Distance",
          }
        };
    // @ts-ignore
    L.control.ruler(options).addTo(map); // ignore typechecking, says "ruler" is not a property even though it gets extended...
  }, [map]);

  return null;
}
