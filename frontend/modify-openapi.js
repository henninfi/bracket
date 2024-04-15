const fs = require('fs').promises;

const filePath = "./openapi.json";
const filePath_output = "./node_modules/@apidevtools/json-schema-ref-parser/dist/openapi.json";

async function modifyOpenAPI() {
  try {
    const data = await fs.readFile(filePath);
    const openapiContent = JSON.parse(data);

    const paths = openapiContent.paths;
    Object.keys(paths).forEach((pathKey) => {
      const pathData = paths[pathKey];
      Object.keys(pathData).forEach((method) => {
        const operation = pathData[method];
        if (operation.tags && operation.tags.length > 0) {
          const tag = operation.tags[0];
          const operationId = operation.operationId;
          const toRemove = `${tag}-`;
          if (operationId.startsWith(toRemove)) {
            operation.operationId = operationId.substring(toRemove.length);
          }
        }
      });
    });

    await fs.writeFile(filePath_output, JSON.stringify(openapiContent, null, 2));
    console.log('OpenAPI specification has been successfully modified.');
  } catch (err) {
    console.error('Error modifying OpenAPI specification:', err);
    process.exit(1);
  }
}

modifyOpenAPI();
