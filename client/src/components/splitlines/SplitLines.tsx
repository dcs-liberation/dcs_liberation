import { Fragment } from "react";

interface SplitLinesProps {
  items: string[];
}

const SplitLines = (props: SplitLinesProps) => {
  return (
    <>
      {props.items.map((text, idx) => {
        return (
          <Fragment key={idx}>
            {text}
            <br />
          </Fragment>
        );
      })}
    </>
  );
};

export default SplitLines;
