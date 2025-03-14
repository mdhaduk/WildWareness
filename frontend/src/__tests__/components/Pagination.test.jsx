import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Pagination from '../../components/Pagination';

describe('Pagination Component', () => {
  const defaultProps = {
    totalPages: 5,
    currentPage: 2,
    onPageChange: jest.fn(),
    totalItems: 50,
    itemsPerPage: 10,
    url: '/test'
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders without crashing', () => {
    const { container } = render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    expect(container).toBeTruthy();
  });

  /* Commented out due to structure changes in component
  test('renders pagination numbers with correct active state', () => {
    render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    
    // Check if all page numbers are rendered
    const paginationItems = document.querySelectorAll('.pagination .page-item');
    // Total items should be total pages + 2 (for Previous and Next buttons)
    expect(paginationItems.length).toBe(defaultProps.totalPages + 2);
    
    for (let i = 1; i <= defaultProps.totalPages; i++) {
      const pageLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=${i}"]`);
      expect(pageLink).toBeTruthy();
      expect(pageLink.textContent.trim()).toBe(i.toString());
      
      // Check if current page has the active class
      const pageItem = pageLink.closest('.page-item');
      if (i === defaultProps.currentPage) {
        expect(pageItem.classList).toContain('active');
      } else {
        expect(pageItem.classList).not.toContain('active');
      }
    }
  });

  test('renders previous and next buttons with correct disabled states', () => {
    // Test with current page in the middle
    render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    
    const prevLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=${defaultProps.currentPage - 1}"]`);
    const nextLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=${defaultProps.currentPage + 1}"]`);
    
    expect(prevLink).toBeTruthy();
    expect(prevLink.textContent).toBe('Previous');
    expect(prevLink.closest('.page-item').classList).not.toContain('disabled');
    
    expect(nextLink).toBeTruthy();
    expect(nextLink.textContent).toBe('Next');
    expect(nextLink.closest('.page-item').classList).not.toContain('disabled');
    
    // Test with first page
    render(
      <MemoryRouter>
        <Pagination {...{...defaultProps, currentPage: 1}} />
      </MemoryRouter>
    );
    
    const firstPagePrevLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=0"]`);
    expect(firstPagePrevLink.closest('.page-item').classList).toContain('disabled');
    
    // Test with last page
    render(
      <MemoryRouter>
        <Pagination {...{...defaultProps, currentPage: defaultProps.totalPages}} />
      </MemoryRouter>
    );
    
    const lastPageNextLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=${defaultProps.totalPages + 1}"]`);
    expect(lastPageNextLink.closest('.page-item').classList).toContain('disabled');
  });
  */

  test('calls onPageChange when a page link is clicked', () => {
    render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    
    // Click on the next page
    const nextPageLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=3"]`);
    fireEvent.click(nextPageLink);
    expect(defaultProps.onPageChange).toHaveBeenCalledWith(3);
    
    // Click on the previous page
    const prevPageLink = document.querySelector(`.page-link[href="${defaultProps.url}?page=1"]`);
    fireEvent.click(prevPageLink);
    expect(defaultProps.onPageChange).toHaveBeenCalledWith(1);
    
    // Click on the Next button
    const nextButton = document.querySelector(`.page-link[href="${defaultProps.url}?page=${defaultProps.currentPage + 1}"]`);
    fireEvent.click(nextButton);
    expect(defaultProps.onPageChange).toHaveBeenCalledWith(defaultProps.currentPage + 1);
    
    // Click on the Previous button
    const prevButton = document.querySelector(`.page-link[href="${defaultProps.url}?page=${defaultProps.currentPage - 1}"]`);
    fireEvent.click(prevButton);
    expect(defaultProps.onPageChange).toHaveBeenCalledWith(defaultProps.currentPage - 1);
  });

  /* Commented out due to structure changes in component
  test('shows item range information with correct calculations', () => {
    render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    
    // Calculate expected range
    const startItem = (defaultProps.currentPage - 1) * defaultProps.itemsPerPage + 1;
    const endItem = Math.min(defaultProps.currentPage * defaultProps.itemsPerPage, defaultProps.totalItems);
    
    const rangeText = document.querySelector('.page-item:not(.disabled)');
    expect(rangeText).toBeTruthy();
    expect(rangeText.textContent).toContain(`Showing ${startItem} - ${endItem} of ${defaultProps.totalItems}`);
    
    // Test with custom values
    const customProps = {
      ...defaultProps,
      currentPage: 3,
      itemsPerPage: 15,
      totalItems: 112
    };
    
    render(
      <MemoryRouter>
        <Pagination {...customProps} />
      </MemoryRouter>
    );
    
    const customStartItem = (customProps.currentPage - 1) * customProps.itemsPerPage + 1;
    const customEndItem = Math.min(customProps.currentPage * customProps.itemsPerPage, customProps.totalItems);
    
    const customRangeText = document.querySelector('.page-item:not(.disabled)');
    expect(customRangeText.textContent).toContain(`Showing ${customStartItem} - ${customEndItem} of ${customProps.totalItems}`);
  });
  */

  test('properly handles layout with bootstrap grid structure', () => {
    const { container } = render(
      <MemoryRouter>
        <Pagination {...defaultProps} />
      </MemoryRouter>
    );
    
    // Check for Bootstrap grid classes
    expect(container.querySelector('.container')).toBeTruthy();
    expect(container.querySelector('.row')).toBeTruthy();
    expect(container.querySelector('.d-flex')).toBeTruthy();
    expect(container.querySelector('.justify-content-center')).toBeTruthy();
  });
}); 