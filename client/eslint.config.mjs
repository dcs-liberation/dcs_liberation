import pkg from "globals";
const { browser, es2021, node } = pkg;
import ts from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  {
    ignores: ["leaflet-ruler.d.ts"],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    plugins: {
      "@typescript-eslint": ts,
      react,
      "react-hooks": reactHooks,
    },
    languageOptions: {
      parser: tsParser,
      ecmaVersion: 2021,
      sourceType: "module",
      globals: { ...browser, ...es2021, ...node },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      ...ts.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",
    },
  },
];
