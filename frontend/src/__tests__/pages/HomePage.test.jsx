import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import HomePage from '../../pages/HomePage';

describe('HomePage Component', () => {
  
  test('renders without crashing', () => {
    const { container } = render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );
    expect(container).toBeTruthy();
  });

  test('renders heading with correct styling and WildWareness title', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('About WildWareness');

    const fireText = heading.querySelector('.fire-text');
    expect(fireText).toBeInTheDocument();
    expect(fireText).toHaveTextContent('WildWareness');
    expect(fireText).toHaveClass('fire-text');
  });

  test('renders the main description with correct content', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    expect(
      screen.getByText(/WildWareness is a web application designed to provide real-time wildfire information/i)
    ).toBeInTheDocument();
    expect(screen.getByText(/emergency shelter locations/i)).toBeInTheDocument();
    expect(screen.getByText(/community-reported fire updates/i)).toBeInTheDocument();
    expect(screen.getByText(/California/i)).toBeInTheDocument();
  });

  test('renders the platform serves section correctly', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    expect(screen.getByText(/Platform serves:/i)).toBeInTheDocument();
    expect(screen.getByText(/People in wildfire-affected areas/i)).toBeInTheDocument();
    expect(screen.getByText(/volunteers and first responders/i)).toBeInTheDocument();
  });

  test('renders the users can section with properly formatted bullet points', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    expect(screen.getByText(/Users can/i)).toBeInTheDocument();

    const listItems = screen.getAllByRole('listitem');
    expect(listItems.length).toBe(3);

    const expectedBulletPoints = [
      'Track active wildfires with real-time data.',
      'Find emergency shelters near affected areas.',
      'View and submit community reports on wildfire conditions.'
    ];

    expectedBulletPoints.forEach(text => {
      expect(screen.getByText(text)).toBeInTheDocument();
    });
  });

  test('renders the carousel with images and controls', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    const carousel = screen.getByTestId('carousel'); 
    expect(carousel).toBeInTheDocument();
    expect(carousel).toHaveClass('carousel');

    // Get only the images inside the carousel
    const images = carousel.querySelectorAll('img'); 
    expect(images.length).toBe(3); 

    const expectedAltTexts = ['Wildfire', 'Emergency Shelter', 'Firefighters'];
    expectedAltTexts.forEach(alt => {
      expect(screen.getByAltText(alt)).toBeInTheDocument();
    });

    // ✅ Fix: Find navigation buttons using role and name
    expect(screen.getByRole('button', { name: /previous/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /next/i })).toBeInTheDocument();
  });

  test('renders three cards with correct titles and links', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    );

    const cardTitles = ['Wildfire Incidents', 'Shelters', 'News Reports'];
    cardTitles.forEach(title => {
      expect(screen.getByText(title)).toBeInTheDocument();
    });

    // Get all "Read More" links
    const links = screen.getAllByRole('link', { name: /Read More/i });
    expect(links.length).toBe(3);

    // Check if the correct links exist
    expect(links[0]).toHaveAttribute('href', '/incidents');
    expect(links[1]).toHaveAttribute('href', '/shelters');
    expect(links[2]).toHaveAttribute('href', '/news');
  });

});
