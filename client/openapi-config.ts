import { ConfigFile } from "@rtk-query/codegen-openapi";

const config: ConfigFile = {
  schemaFile: "http://[::1]:16880/openapi.json",
  apiFile: "./src/api/baseApi.ts",
  apiImport: "baseApi",
  outputFile: "./src/api/_liberationApi.ts",
  exportName: "_liberationApi",
  hooks: true,
};

export default config;
