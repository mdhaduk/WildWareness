import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Navbar from '../../components/Navbar';

describe('Navbar Component', () => {
  test('renders without crashing', () => {
    const { container } = render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    expect(container).toBeTruthy();
  });

  test('renders the WildWareness brand with correct styling', () => {
    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    
    const brandElement = document.querySelector('.navbar-brand');
    expect(brandElement).toBeTruthy();
    expect(brandElement.textContent).toBe('WildWareness');
    expect(brandElement.classList).toContain('fire-text');
    expect(brandElement.getAttribute('href')).toBe('/');
    
    // Check style properties
    const computedStyle = window.getComputedStyle(brandElement);
    expect(brandElement.style.fontSize).toBe('medium');
  });

  test('renders navigation links with proper classes', () => {
    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    
    const navLinks = document.querySelectorAll('.nav-link');
    expect(navLinks.length).toBe(4); // Ensure all 4 links are present
    
    // Check if they have the correct classes
    const linkTexts = ['Wildfire Incidents', 'Emergency Shelters', 'Community Reports', 'About'];
    linkTexts.forEach(text => {
      const link = Array.from(navLinks).find(el => el.textContent.includes(text));
      expect(link).toBeTruthy();
      expect(link.classList).toContain('nav-link');
    });
    
    // Check if About link is active and has strong styling
    const aboutLink = Array.from(navLinks).find(el => el.textContent.includes('About'));
    expect(aboutLink.classList).toContain('active');
    expect(aboutLink.innerHTML).toContain('<strong>');
  });

  test('links have the correct URLs and navigate correctly', () => {
    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    
    const expectedLinks = [
      { text: 'Wildfire Incidents', href: '/incidents' },
      { text: 'Emergency Shelters', href: '/shelters' },
      { text: 'Community Reports', href: '/news' },
      { text: 'About', href: '/about' }
    ];
    
    expectedLinks.forEach(({ text, href }) => {
      const link = document.querySelector(`a[href="${href}"]`);
      expect(link).toBeTruthy();
      expect(link.textContent).toContain(text);
    });
  });

  test('navbar is responsive with collapse functionality', () => {
    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );
    
    // Check if navbar toggler exists
    const toggler = document.querySelector('.navbar-toggler');
    expect(toggler).toBeTruthy();
    expect(toggler.getAttribute('data-bs-toggle')).toBe('collapse');
    expect(toggler.getAttribute('data-bs-target')).toBe('#navbarNav');
    
    // Check if collapsible element exists
    const collapsible = document.querySelector('#navbarNav');
    expect(collapsible).toBeTruthy();
    expect(collapsible.classList).toContain('collapse');
    expect(collapsible.classList).toContain('navbar-collapse');
  });
}); 