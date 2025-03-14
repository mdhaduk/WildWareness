import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import Pagination from '../components/Pagination';

function NewsReports() {
    const [reports, setReports] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchParams, setSearchParams] = useSearchParams();

    // Extract page parameter from URL
    const pageParam = parseInt(searchParams.get("page")) || 1;

    useEffect(() => {
        const fetchReports = async () => {
            try {
                console.log("Fetching data for page:", pageParam);
                const response = await axios.get(`http://127.0.0.1:5000/news`, {
                    params: { page: pageParam, size: itemsPerPage },
                });

                console.log(response.data); // Debugging
                setReports(response.data.incidents);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setItemsPerPage(response.data.pagination.size);
            } catch (error) {
                console.error("Error fetching wildfire instances:", error);
            }
        };

        fetchReports();
    }, [pageParam]); // ✅ Correct dependency to avoid infinite loops

    const handlePageChange = (page) => {
        // Update the URL and trigger a re-render
        setSearchParams({ page });
    };

    // Function to truncate text
    const truncateText = (text, maxLength = 45) => {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.slice(0, maxLength) + '...';
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">News Reports</h2>

            <div className="row">
                {reports.length > 0 ? (
                    reports.map((report) => (
                        <div key={report.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={report.image_url} alt={report.title}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item" style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                                        <strong style={{ marginBottom: '4px' }}>Title:</strong>
                                        <div 
                                            title={report.title} 
                                            className="truncated-title"
                                            style={{ 
                                                width: '100%'
                                            }}
                                            data-full-title={report.title}
                                        >
                                            {truncateText(report.title, 45)}
                                        </div>
                                    </li>
                                    <li className="list-group-item"><strong>Source:</strong> {report.source}</li>
                                    <li className="list-group-item"><strong>Date:</strong> {report.published_at}</li>
                                    <li className="list-group-item"><strong>Author:</strong> {report.author}</li>
                                    <li className="list-group-item"><strong>Categories:</strong> {report.categories}</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/news/${report.id}`} className="btn btn-primary">Read More</Link>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-center">Loading...</p>
                )}
            </div>

            {/* Pagination */}
            <div className="d-flex justify-content-center mt-4">
                <Pagination 
                    totalPages={totalPages} 
                    currentPage={pageParam} 
                    onPageChange={handlePageChange}  
                    totalItems={totalItems} 
                    itemsPerPage={itemsPerPage} 
                    url={'/news'}
                />
            </div>
        </div>
    );
}

export default NewsReports;
