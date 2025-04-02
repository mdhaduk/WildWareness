const Pagination = ({ totalPages, currentPage, onPageChange, totalItems, itemsPerPage }) => {
  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      onPageChange(page);
    }
  };

  const renderPageItem = (page) => (
    <li key={page} className={`page-item ${page === currentPage ? 'active' : ''}`}>
      <button className="page-link" onClick={() => handlePageChange(page)}>
        {page}
      </button>
    </li>
  );

  const createPaginationItems = () => {
    const pages = [];
    const pageWindow = 1;

    if (1 === currentPage) {
      pages.push(renderPageItem(1));
    } else {
      pages.push(renderPageItem(1));
    }

    if (currentPage > 2 + pageWindow) {
      pages.push(<li key="start-ellipsis" className="page-item disabled"><span className="page-link">...</span></li>);
    }

    const start = Math.max(2, currentPage - pageWindow);
    const end = Math.min(totalPages - 1, currentPage + pageWindow);

    for (let i = start; i <= end; i++) {
      pages.push(renderPageItem(i));
    }

    if (currentPage < totalPages - (1 + pageWindow)) {
      pages.push(<li key="end-ellipsis" className="page-item disabled"><span className="page-link">...</span></li>);
    }

    if (totalPages > 1) {
      pages.push(renderPageItem(totalPages));
    }

    return pages;
  };

  if (totalPages <= 1) return null;

  return (
    <div className="container text-center">
      <div className="row">
        <div className="d-flex justify-content-center my-4">
          <nav>
            <ul className="pagination flex-wrap">
              {/* Previous Button */}
              <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                <button className="page-link" onClick={() => handlePageChange(currentPage - 1)}>
                  Previous
                </button>
              </li>

              {/* Page Items */}
              {createPaginationItems()}

              {/* Next Button */}
              <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                <button className="page-link" onClick={() => handlePageChange(currentPage + 1)}>
                  Next
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <div className="row">
        <h4 className="page-item">
          Showing {startItem} - {endItem} of {totalItems}
        </h4>
      </div>
    </div>
  );
};

export default Pagination;
