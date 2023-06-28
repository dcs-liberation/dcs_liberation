import mergeRefs from "./mergeRefs";

describe("mergeRefs", () => {
  it("merges all kinds of refs", () => {
    const referent = "foobar";
    const ref = { current: null };
    var callbackResult = null;
    const callbackRef = (node: string | null) => {
      if (node != null) {
        callbackResult = node;
      }
    };
    mergeRefs(ref, callbackRef)(referent);
    expect(callbackResult).toEqual("foobar");
    expect(ref.current).toEqual("foobar");
  });
});
