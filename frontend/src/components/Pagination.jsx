import React from "react";
import { Pagination } from "react-bootstrap";

const PaginationComponent = ({ totalPages, currentPage, onPageChange }) => {
  // Check if totalPages is valid
  if (typeof totalPages !== "number" || totalPages <= 0) {
    console.error("Invalid totalPages value:", totalPages);
    return null; // Prevent rendering if totalPages is invalid
  }

  const handlePageChange = (pageNumber) => {
    if (pageNumber >= 1 && pageNumber <= totalPages) {
      onPageChange(pageNumber);
    }
  };

  // Generate page range to show: 2 before and 2 after currentPage, plus the first and last page
  let startPage = Math.max(currentPage - 2, 1);
  let endPage = Math.min(currentPage + 2, totalPages);

  // Handle the scenario where there are less than 5 pages in total
  if (totalPages <= 5) {
    startPage = 1;
    endPage = totalPages;
  }

  // Create the page numbers array
  const pages = [];
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return (
    <Pagination className="justify-content-center" size="lg">
      
      {/* Previous Page */}
      <Pagination.Prev
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
      />

      {/* Show "1" for the first page if it's not already in the range */}
      {startPage > 1 && (
        <>
          <Pagination.Item onClick={() => handlePageChange(1)}>1</Pagination.Item>
          <Pagination.Ellipsis />
        </>
      )}

      {/* Display pages in range */}
      {pages.map((pageNumber) => (
        <Pagination.Item
          key={pageNumber}
          active={pageNumber === currentPage}
          onClick={() => handlePageChange(pageNumber)}
        >
          {pageNumber}
        </Pagination.Item>
      ))}

      {/* Show the last page if it's not already in the range */}
      {endPage < totalPages && (
        <>
          <Pagination.Ellipsis />
          <Pagination.Item onClick={() => handlePageChange(totalPages)}>
            {totalPages}
          </Pagination.Item>
        </>
      )}

      {/* Next Page */}
      <Pagination.Next
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      />
      
    </Pagination>
  );
};

export default PaginationComponent;
