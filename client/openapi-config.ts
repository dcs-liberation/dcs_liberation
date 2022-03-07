import { ConfigFile } from "@rtk-query/codegen-openapi";

const config: ConfigFile = {
  schemaFile: "http://[::1]:5000/openapi.json",
  apiFile: "./src/api/baseApi.ts",
  apiImport: "baseApi",
  outputFile: "./src/api/liberationApi.ts",
  exportName: "liberationApi",
  hooks: true,
};

export default config;
