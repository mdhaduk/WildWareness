import { screen, fireEvent } from '@testing-library/react';
import { describe, test, expect, jest } from '@jest/globals';
import Pagination from '../components/Pagination';
import { renderWithRouter } from './testUtils';

describe('Pagination Component', () => {
  const mockOnPageChange = jest.fn();
  
  beforeEach(() => {
    mockOnPageChange.mockClear();
  });

  test('renders pagination with previous and next links', () => {
    renderWithRouter(<Pagination totalItems={50} itemsPerPage={10} onPageChange={mockOnPageChange} />);
    
    const prevLink = screen.getByText('Previous');
    const nextLink = screen.getByText('Next');
    
    expect(prevLink).toBeInTheDocument();
    expect(nextLink).toBeInTheDocument();
  });

  test('renders showing text with total items', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const showingText = screen.getByText(/Showing.*of 30/);
    expect(showingText).toBeInTheDocument();
  });

  test('has correct href on next link', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const nextLink = screen.getByText('Next');
    expect(nextLink).toHaveAttribute('href', expect.stringContaining('page='));
  });

  test('has correct href on previous link', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={2} onPageChange={mockOnPageChange} />);
    
    const prevLink = screen.getByText('Previous');
    expect(prevLink).toHaveAttribute('href', expect.stringContaining('page='));
  });

  test('previous link parent has disabled class on first page', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const prevLink = screen.getByText('Previous');
    const prevLinkParent = prevLink.closest('li');
    
    expect(prevLinkParent).toHaveClass('disabled');
  });

  test('renders pagination container with bootstrap classes', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const paginationList = screen.getByRole('list');
    expect(paginationList).toHaveClass('pagination');
  });

  test('renders navigation element', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const navElement = screen.getByRole('navigation');
    expect(navElement).toBeInTheDocument();
  });

  test('renders page items with correct classes', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const pageItems = screen.getAllByRole('listitem');
    pageItems.forEach(item => {
      expect(item).toHaveClass('page-item');
    });
  });

  test('renders page links with correct classes', () => {
    renderWithRouter(<Pagination totalItems={30} itemsPerPage={10} currentPage={1} onPageChange={mockOnPageChange} />);
    
    const pageLinks = screen.getAllByRole('link');
    pageLinks.forEach(link => {
      expect(link).toHaveClass('page-link');
    });
  });
}); 