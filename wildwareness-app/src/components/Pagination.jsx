import { Link } from 'react-router-dom';

const Pagination = ({ totalPages, currentPage, onPageChange, totalItems, itemsPerPage , url}) => {
    const startItem = (currentPage - 1) * itemsPerPage + 1;
    const endItem = Math.min(currentPage * itemsPerPage, totalItems);
  
    const handlePageChange = (page) => {
      if (page >= 1 && page <= totalPages) {
        onPageChange(page);
      }
    };
  
    // Generate pagination items based on totalPages
    const paginationItems = [];
    for (let i = 1; i <= totalPages; i++) {
      paginationItems.push(
        <li key={i} className={`page-item ${i === currentPage ? 'active' : ''}`}>
              <Link className="page-link" to={`${url}?page=${i}`} onClick={() => handlePageChange(i)}>
                {i}
              </Link>
        </li>
      );
    }
  
    return (
      <div className="container text-center">
      <div className="row">
        <div className="d-flex justify-content-center my-4">
            <nav>
              <ul className="pagination">
                {/* Previous Button */}
                <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
                <Link className="page-link" to={`${url}?page=${currentPage - 1}`} onClick={() => handlePageChange(currentPage - 1)}>
                    Previous
                  </Link>
                </li>
  
                {/* Page Number Buttons */}
                {paginationItems}
  
                {/* Next Button */}
                <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
                  <Link className="page-link" to={`${url}?page=${currentPage + 1}`} onClick={() => handlePageChange(currentPage + 1)}>
                    Next
                  </Link>
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