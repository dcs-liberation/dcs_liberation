interface LocationTooltipTextProps {
  name: string;
}

export const LocationTooltipText = (props: LocationTooltipTextProps) => {
  return <h3 style={{ margin: 0 }}>{props.name}</h3>;
};

export default LocationTooltipText;
