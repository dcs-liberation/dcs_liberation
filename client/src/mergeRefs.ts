import { ForwardedRef } from "react";

const mergeRefs = <T extends any>(...refs: ForwardedRef<T>[]) => {
  return (node: T) => {
    for (const ref of refs) {
      if (ref == null) {
      } else if (typeof ref === "function") {
        ref(node);
      } else {
        ref.current = node;
      }
    }
  };
};

export default mergeRefs;
