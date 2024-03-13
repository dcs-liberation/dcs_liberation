// Ignoring eslint here because we know L.control.ruler is used in Ruler.tsx

interface CircleMarker {
  color: string;
  radius: number;
}

interface LineStyle {
  color: string;
  dashArray: string;
}

interface LengthUnit {
  display: string;
  decimal: number;
  factor: number?;
  label: string;
}

interface AngleUnit {
  display: string;
  decimal: number;
  factor: number?;
  label: string;
}

interface RulerOptions {
  position?: string;
  circleMarker?: CircleMarker;
  lineStyle?: LineStyle;
  lengthUnit?: LengthUnit;
  angleUnit?: AngleUnit;
}

declare namespace L.control {
  function ruler (options: RulerOptions) : L.Control {}
}
