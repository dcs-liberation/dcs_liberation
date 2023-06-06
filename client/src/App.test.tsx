import App from "./App";
import { setupStore } from "./app/store";
import { render } from "@testing-library/react";
import { Provider } from "react-redux";

test("app renders", () => {
  render(
    <Provider store={setupStore()}>
      <App />
    </Provider>
  );
});
