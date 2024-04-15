// generateClientCore.js
const { execSync } = require('child_process');
const path = require('path');

// Construct the absolute path to openapi.json
const openapiPath = path.resolve(__dirname, 'openapi.json');

// Update the command to include the generator name and additional properties correctly
const command = `openapi-generator-cli generate -i "${openapiPath}" -g typescript-axios --output ./src/client --skip-validate-spec --additional-properties=useOptions=true,useUnionTypes=true`;

// Execute the command
try {
  execSync(command, { stdio: 'inherit' }); // Use stdio: 'inherit' to display output in the terminal
  console.log('Client generated successfully.');
} catch (error) {
  console.error('Failed to generate client:', error);
  process.exit(1); // Exit with an error code if the command fails
}
