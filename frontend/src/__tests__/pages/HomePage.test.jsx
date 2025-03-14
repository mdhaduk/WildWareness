import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import HomePage from '../../pages/HomePage';

// Simple test that just checks if the component renders without crashing
describe('HomePage Component', () => {
  test('renders without crashing', () => {
    // This will throw an error if the component fails to render
    const { container } = render(<HomePage />);
    // Simple assertion that the container is in the document
    expect(container).toBeTruthy();
  });

  test('renders heading with correct styling and WildWareness title', () => {
    const { container } = render(<HomePage />);
    
    // Check heading structure
    const heading = container.querySelector('h1');
    expect(heading).toBeTruthy();
    expect(heading.textContent).toContain('About');
    
    // Check the title with the fire-text class
    const fireText = heading.querySelector('.fire-text');
    expect(fireText).toBeTruthy();
    expect(fireText.textContent).toBe('WildWareness');
    expect(fireText.classList).toContain('fire-text');
  });

  test('renders the main description with correct content and styling', () => {
    const { container } = render(<HomePage />);
    
    // Find the paragraph with the description
    const paragraphs = container.querySelectorAll('p');
    const descriptionParagraph = Array.from(paragraphs).find(
      p => p.textContent.includes('WildWareness is a web application designed to provide real-time wildfire information')
    );
    
    expect(descriptionParagraph).toBeTruthy();
    expect(descriptionParagraph.textContent).toContain('emergency shelter locations');
    expect(descriptionParagraph.textContent).toContain('community-reported fire updates');
    expect(descriptionParagraph.textContent).toContain('California');
  });

  test('renders the platform serves section with proper formatting', () => {
    const { container } = render(<HomePage />);
    
    // Find the paragraph with the platform serves section
    const platformServesParagraph = Array.from(container.querySelectorAll('p')).find(
      p => p.textContent.includes('Platform serves:')
    );
    
    expect(platformServesParagraph).toBeTruthy();
    
    // Check for strong element
    const strongElement = platformServesParagraph.querySelector('strong');
    expect(strongElement).toBeTruthy();
    expect(strongElement.textContent).toBe('Platform serves:');
    
    // Check the description content
    expect(platformServesParagraph.textContent).toContain('People in wildfire-affected areas');
    expect(platformServesParagraph.textContent).toContain('volunteers and first responders');
  });

  test('renders the users can section with properly formatted bullet points', () => {
    const { container } = render(<HomePage />);
    
    // Find the users can paragraph
    const usersCanParagraph = Array.from(container.querySelectorAll('p')).find(
      p => p.textContent.includes('Users can')
    );
    
    expect(usersCanParagraph).toBeTruthy();
    expect(usersCanParagraph.querySelector('strong')).toBeTruthy();
    
    // Check the unordered list
    const bulletList = container.querySelector('ul');
    expect(bulletList).toBeTruthy();
    expect(bulletList.classList).toContain('text-start');
    
    // Check the list items
    const listItems = bulletList.querySelectorAll('li');
    expect(listItems.length).toBe(3);
    
    // Check content of each list item
    const expectedBulletPoints = [
      'Track active wildfires with real-time data.',
      'Find emergency shelters near affected areas.',
      'View and submit community reports on wildfire conditions.'
    ];
    
    expectedBulletPoints.forEach((expectedText, index) => {
      expect(listItems[index].textContent).toBe(expectedText);
    });
  });

  test('renders fully functional carousel with correct images and controls', () => {
    const { container } = render(<HomePage />);
    
    // Check carousel container
    const carousel = container.querySelector('#carouselExampleAutoplaying');
    expect(carousel).toBeTruthy();
    expect(carousel.classList).toContain('carousel');
    expect(carousel.classList).toContain('slide');
    expect(carousel.getAttribute('data-bs-ride')).toBe('carousel');
    
    // Check carousel style dimensions - fixing the style name to match the actual implementation
    const carouselStyle = carousel.getAttribute('style');
    expect(carouselStyle).toContain('max-width');
    expect(carouselStyle).toContain('max-height');
    
    // Check carousel items
    const carouselItems = carousel.querySelectorAll('.carousel-item');
    expect(carouselItems.length).toBe(3);
    expect(carouselItems[0].classList).toContain('active');
    
    // Check images
    const images = carousel.querySelectorAll('img');
    expect(images.length).toBe(3);
    
    // Check alt text for each image
    const expectedAltTexts = ['Wildfire', 'Emergency Shelter', 'Firefighters'];
    expectedAltTexts.forEach((altText, index) => {
      expect(images[index].getAttribute('alt')).toBe(altText);
    });
    
    // Check if all images have the proper bootstrap classes
    images.forEach(img => {
      expect(img.classList).toContain('d-block');
      expect(img.classList).toContain('w-100');
    });
    
    // Check carousel controls
    const prevButton = carousel.querySelector('.carousel-control-prev');
    const nextButton = carousel.querySelector('.carousel-control-next');
    
    expect(prevButton).toBeTruthy();
    expect(prevButton.getAttribute('data-bs-slide')).toBe('prev');
    expect(prevButton.querySelector('.carousel-control-prev-icon')).toBeTruthy();
    expect(prevButton.querySelector('.visually-hidden')).toBeTruthy();
    expect(prevButton.querySelector('.visually-hidden').textContent).toBe('Previous');
    
    expect(nextButton).toBeTruthy();
    expect(nextButton.getAttribute('data-bs-slide')).toBe('next');
    expect(nextButton.querySelector('.carousel-control-next-icon')).toBeTruthy();
    expect(nextButton.querySelector('.visually-hidden')).toBeTruthy();
    expect(nextButton.querySelector('.visually-hidden').textContent).toBe('Next');
  });

  test('layout uses Bootstrap grid system correctly', () => {
    const { container } = render(<HomePage />);
    
    // Check main container
    const mainContainer = container.querySelector('.container-fluid');
    expect(mainContainer).toBeTruthy();
    expect(mainContainer.classList).toContain('hero-section');
    
    // Check row
    const row = mainContainer.querySelector('.row');
    expect(row).toBeTruthy();
    expect(row.classList).toContain('w-100');
    
    // Check columns
    const columns = row.querySelectorAll('.col-lg-6');
    expect(columns.length).toBe(2);
    
    // Check first column (text content)
    const textColumn = columns[0];
    expect(textColumn.classList).toContain('d-flex');
    expect(textColumn.classList).toContain('flex-column');
    expect(textColumn.classList).toContain('align-items-center');
    expect(textColumn.classList).toContain('justify-content-center');
    expect(textColumn.classList).toContain('text-center');
    expect(textColumn.classList).toContain('px-5');
    
    // Check second column (carousel)
    const carouselColumn = columns[1];
    expect(carouselColumn.classList).toContain('d-flex');
    expect(carouselColumn.classList).toContain('align-items-center');
    expect(carouselColumn.classList).toContain('justify-content-center');
  });
}); 