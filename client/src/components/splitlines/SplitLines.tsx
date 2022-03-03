interface SplitLinesProps {
  items: string[];
}

const SplitLines = (props: SplitLinesProps) => {
  return (
    <>
      {props.items.map((text) => {
        return (
          <>
            {text}
            <br />
          </>
        );
      })}
    </>
  );
};

export default SplitLines;
