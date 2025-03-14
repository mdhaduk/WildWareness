import { render, screen } from '@testing-library/react';
import { describe, test, expect, jest, beforeEach, afterEach } from '@jest/globals';
import Map from '../components/Map';
import { mockResponses } from './testUtils';

// Mock the Leaflet library with ESM-compatible mocking approach
jest.unstable_mockModule('leaflet', () => ({
  map: jest.fn(() => ({
    setView: jest.fn(),
    remove: jest.fn()
  })),
  tileLayer: jest.fn(() => ({
    addTo: jest.fn()
  })),
  marker: jest.fn(() => ({
    addTo: jest.fn(),
    bindPopup: jest.fn(() => ({
      openPopup: jest.fn()
    }))
  })),
  icon: jest.fn(),
  divIcon: jest.fn()
}));

// Create mock DOM elements for map
beforeEach(() => {
  // Create a map container element
  const mapContainer = document.createElement('div');
  mapContainer.id = 'map';
  document.body.appendChild(mapContainer);
});

// Cleanup after each test
afterEach(() => {
  const mapElement = document.getElementById('map');
  if (mapElement) {
    document.body.removeChild(mapElement);
  }
  jest.clearAllMocks();
});

describe('Map Component', () => {
  const mockWildfires = mockResponses.wildfires;
  
  test('renders map container with correct ID', () => {
    render(<Map wildfires={mockWildfires} />);
    const mapElement = document.getElementById('map');
    expect(mapElement).toBeInTheDocument();
  });
  
  test('renders loading message when wildfires are null', () => {
    render(<Map wildfires={null} />);
    const loadingElement = screen.getByText(/Loading map.../i);
    expect(loadingElement).toBeInTheDocument();
  });
  
  test('renders loading message when wildfires array is empty', () => {
    render(<Map wildfires={[]} />);
    const loadingElement = screen.getByText(/Loading map.../i);
    expect(loadingElement).toBeInTheDocument();
  });
  
  test('renders map container when wildfires data is provided', () => {
    render(<Map wildfires={mockWildfires} />);
    const mapContainer = document.getElementById('map');
    expect(mapContainer).toBeInTheDocument();
  });
}); 