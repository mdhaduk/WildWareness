// Helper functions for testing

import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Render component with Router context
export function renderWithRouter(ui, { route = '/' } = {}) {
  window.history.pushState({}, 'Test page', route);
  
  return {
    ...render(
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    )
  };
}

// Mock responses for APIs
export const mockResponses = {
  wildfires: [
    {
      id: 1,
      name: "Cedar Fire",
      county: "San Diego",
      location: "Cleveland National Forest",
      year: "2003",
      acres_burned: "273,246",
      url: "https://example.com/cedar-fire",
      latitude: "32.8801",
      longitude: "-116.4813",
      description: "The Cedar Fire was a massive wildfire that burned in San Diego County, California.",
      ongoing: false
    },
    {
      id: 2,
      name: "Dixie Fire",
      county: "Butte",
      location: "Feather River Canyon",
      year: "2021",
      acres_burned: "963,309",
      url: "https://example.com/dixie-fire",
      latitude: "40.0131",
      longitude: "-121.2030",
      description: "The Dixie Fire was a large wildfire that burned in Butte County, California.",
      ongoing: false
    }
  ],
  
  shelters: [
    {
      id: 1,
      name: "San Diego Emergency Shelter",
      address: "123 Main St, San Diego, CA",
      phone: "555-123-4567",
      website: "https://example.com/sd-shelter",
      rating: "4.5",
      reviews: JSON.stringify([{user: "John", rating: 4, comment: "Good facilities"}]),
      imageUrl: "https://example.com/shelter1.jpg",
      description: "Emergency shelter in San Diego with capacity for 200 people",
      county: "San Diego",
      max_occupancy: 200
    },
    {
      id: 2,
      name: "Butte County Evacuation Center",
      address: "456 Oak St, Chico, CA",
      phone: "555-987-6543",
      website: "https://example.com/butte-shelter",
      rating: "4.0",
      reviews: JSON.stringify([{user: "Jane", rating: 4, comment: "Well organized"}]),
      imageUrl: "https://example.com/shelter2.jpg",
      description: "Evacuation center with pet facilities",
      county: "Butte",
      max_occupancy: 150
    }
  ],
  
  news: [
    {
      id: 1,
      title: "Wildfire Updates for Northern California",
      description: "Latest news on wildfires affecting Northern California regions",
      source: "CalFire News",
      published_at: "2023-07-15",
      url: "https://example.com/news1"
    },
    {
      id: 2,
      title: "Evacuations Ordered in Southern California",
      description: "Mandatory evacuations have been ordered in parts of Southern California",
      source: "Emergency Services",
      published_at: "2023-08-20",
      url: "https://example.com/news2"
    }
  ]
}; 