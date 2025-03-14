// This file is automatically loaded by Jest
import '@testing-library/jest-dom';
import { jest } from '@jest/globals';
import { TextEncoder, TextDecoder } from 'util';

// Add TextEncoder/TextDecoder to global for React Router
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mock global fetch for API tests
global.fetch = jest.fn(() => 
  Promise.resolve({
    json: () => Promise.resolve({}),
    ok: true,
    status: 200
  })
);

// Reset mocks between tests
beforeEach(() => {
  global.fetch.mockClear();
});

// Silence React 19 act() warnings that might occur with testing-library
const originalError = console.error;
console.error = (...args) => {
  if (args[0]?.includes?.('act(...)') || args[0]?.includes?.('Warning: ReactDOM.render')) {
    return;
  }
  originalError(...args);
}; 