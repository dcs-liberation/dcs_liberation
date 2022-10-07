import App from "./App";
import { store } from "./app/store";
import { render } from "@testing-library/react";
import { Provider } from "react-redux";

test("app renders", () => {
  render(
    <Provider store={store}>
      <App />
    </Provider>
  );
});
