// jest-dom adds custom jest matchers for asserting on DOM nodes
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';
import { jest } from '@jest/globals';

// Mock fetch globally
global.fetch = jest.fn();

// Add TextEncoder/TextDecoder polyfill for Node.js environment
global.TextEncoder = function TextEncoder() {
  return {
    encode: function encode(str) {
      const buf = new Uint8Array(str.length);
      for (let i = 0; i < str.length; i++) {
        buf[i] = str.charCodeAt(i);
      }
      return buf;
    }
  };
};

global.TextDecoder = function TextDecoder() {
  return {
    decode: function decode(buf) {
      let result = '';
      for (let i = 0; i < buf.length; i++) {
        result += String.fromCharCode(buf[i]);
      }
      return result;
    }
  };
};

// Set up browser environment globals that might be missing in Jest
if (typeof window !== 'undefined') {
  // Mock URL.createObjectURL
  window.URL.createObjectURL = jest.fn().mockReturnValue('mock-url');
  
  // Mock URL.revokeObjectURL
  window.URL.revokeObjectURL = jest.fn();
  
  // Add ResizeObserver mock (often needed for UI components)
  window.ResizeObserver = jest.fn().mockImplementation(() => ({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
  }));
  
  // Mock matchMedia for responsive design components
  window.matchMedia = jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  }));
}

// Reset mocks between tests
beforeEach(() => {
  if (global.fetch) {
    global.fetch.mockClear();
  }
}); 