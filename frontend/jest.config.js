export default {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  transformIgnorePatterns: [
    'node_modules/(?!(react|react-dom)/)'
  ],
  moduleFileExtensions: ['js', 'jsx'],
  testMatch: ['**/__tests__/**/*.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  // Prevent React version conflicts
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons'],
  },
  // Use this to avoid incompatibilities
  resolver: '<rootDir>/test/resolver.cjs'
}; 