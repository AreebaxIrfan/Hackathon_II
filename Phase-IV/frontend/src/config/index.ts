/**
 * Configuration management for the Chat Interface
 */

// Define environment variables with defaults
const config = {
  apiUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api',
  openAiApiKey: process.env.REACT_APP_OPENAI_API_KEY || '',
  mcpServerUrl: process.env.REACT_APP_MCP_SERVER_URL || 'http://localhost:8001',
  authUrl: process.env.REACT_APP_BETTER_AUTH_URL || 'http://localhost:3000',
  environment: process.env.NODE_ENV || 'development',
  logLevel: process.env.REACT_APP_LOG_LEVEL || 'info'
};

// Validate required configuration values
const requiredConfig = ['apiUrl', 'openAiApiKey'];
const missingConfig = requiredConfig.filter(key => !config[key as keyof typeof config]);

if (missingConfig.length > 0) {
  console.warn(`Warning: Missing required configuration values: ${missingConfig.join(', ')}`);
}

// Export the configuration
export default config;

// Export a validation function to check if configuration is valid
export const validateConfig = (): boolean => {
  const requiredValues = [
    config.apiUrl,
    config.openAiApiKey
  ];

  return requiredValues.every(value => !!value && value !== '');
};