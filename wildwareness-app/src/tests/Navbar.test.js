import { screen } from '@testing-library/react';
import { describe, test, expect, jest, beforeEach } from '@jest/globals';
import Navbar from '../components/Navbar';
import { renderWithRouter } from './testUtils';

// Mock the Bootstrap JS using ESM compatible mocking
jest.unstable_mockModule('bootstrap/dist/js/bootstrap.bundle.min.js', () => ({}));

// Reset all mocks before each test
beforeEach(() => {
  jest.clearAllMocks();
});

describe('Navbar Component', () => {
  test('renders navbar brand', () => {
    renderWithRouter(<Navbar />);
    const brandElement = screen.getByText(/WildWareness/i);
    expect(brandElement).toBeInTheDocument();
  });

  test('renders all navigation links', () => {
    renderWithRouter(<Navbar />);
    
    const incidentsLink = screen.getByText(/Wildfire Incidents/i);
    const sheltersLink = screen.getByText(/Emergency Shelters/i);
    const newsLink = screen.getByText(/Community Reports/i);
    const aboutLink = screen.getByText(/About/i);
    
    expect(incidentsLink).toBeInTheDocument();
    expect(sheltersLink).toBeInTheDocument();
    expect(newsLink).toBeInTheDocument();
    expect(aboutLink).toBeInTheDocument();
  });
  
  test('navigation links have correct href attributes', () => {
    renderWithRouter(<Navbar />);
    
    const incidentsLink = screen.getByText(/Wildfire Incidents/i);
    const sheltersLink = screen.getByText(/Emergency Shelters/i);
    const newsLink = screen.getByText(/Community Reports/i);
    const aboutLink = screen.getByText(/About/i);
    
    expect(incidentsLink.closest('a')).toHaveAttribute('href', '/incidents');
    expect(sheltersLink.closest('a')).toHaveAttribute('href', '/shelters');
    expect(newsLink.closest('a')).toHaveAttribute('href', '/news');
    expect(aboutLink.closest('a')).toHaveAttribute('href', '/about');
  });
  
  test('about link should have active class', () => {
    renderWithRouter(<Navbar />);
    
    const aboutLink = screen.getByText(/About/i);
    expect(aboutLink.closest('a')).toHaveClass('active');
  });
  
  test('about link should be wrapped in a strong element', () => {
    renderWithRouter(<Navbar />);
    
    const aboutLink = screen.getByText(/About/i);
    expect(aboutLink.tagName).toBe('STRONG');
  });

  test('navbar should have proper Bootstrap classes', () => {
    renderWithRouter(<Navbar />);
    
    const navElement = screen.getByRole('navigation');
    expect(navElement).toHaveClass('navbar');
    expect(navElement).toHaveClass('navbar-expand-lg');
  });

  test('navbar container should have fluid class', () => {
    renderWithRouter(<Navbar />);
    
    const containerDiv = screen.getByText(/WildWareness/i).closest('.container-fluid');
    expect(containerDiv).toBeInTheDocument();
    expect(containerDiv).toHaveClass('container-fluid');
  });
}); 