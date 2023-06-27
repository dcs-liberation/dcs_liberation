import SplitLines from "./SplitLines";
import { screen } from "@testing-library/dom";
import { render } from "@testing-library/react";

describe("SplitLines", () => {
  it("joins items with line break tags", () => {
    render(
      <div data-testid={"container"}>
        <SplitLines items={["foo", "bar", "baz"]} />
      </div>
    );

    const container = screen.getByTestId("container");
    expect(container).toContainHTML("foo<br />bar<br />baz<br />");
  });
});
