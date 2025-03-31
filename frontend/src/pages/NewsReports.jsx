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
    const [loading, setLoading] = useState(false); // Loading state to handle loading spinner
    const [error, setError] = useState(null);
    const [searchParams, setSearchParams] = useSearchParams();

    // Sorting and Filtering States
    const [sortBy, setSortBy] = useState('title');
    const [order, setOrder] = useState('asc');
    const [source, setSource] = useState('');
    const [author, setAuthor] = useState('');
    const [date, setDate] = useState('');

    // Extract page parameter from URL
    const pageParam = parseInt(searchParams.get("page")) || 1;
    // const query = useLocation();

    // Fetch reports from the API with the current filters applied
    useEffect(() => {
        console.log("Working")
        const fetchReports = async () => {
            setLoading(true); // Start loading before fetching data
            try {
                console.log("Fetching data for page:", pageParam);
                const params = {
                    page: pageParam,
                    size: itemsPerPage,
                    source: source,
                };
                const response = await axios.get(`http://localhost:5000/news`, { params });

                console.log(response.data); // Debugging
                setReports(response.data.incidents); // Update reports to the filtered results
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setItemsPerPage(response.data.pagination.size);
            } catch (error) {
                console.error("Error fetching news reports:", error);
                setError(error);
            } finally {
                setLoading(false); // Stop loading after fetching is complete
            }
        };

        fetchReports();
    }, [pageParam, itemsPerPage, source]); // Dependencies to trigger refetch when state changes

    // // Update URL based on filters and page
    // useEffect(() => {
    //     const queryParams = new URLSearchParams();

    //     if (sortBy) queryParams.append('sortBy', sortBy);
    //     if (order) queryParams.append('order', order);
    //     if (source) queryParams.append('source', source);
    //     if (author) queryParams.append('author', author);
    //     if (date) queryParams.append('date', date);
    //     queryParams.append('page', pageParam);

    //     navigate(`/news?${queryParams.toString()}`);
    // }, [pageParam, sortBy, order, source, author, date]);

    const handlePageChange = (page) => {
        setSearchParams({ page });
    };

    // Handle filter change and update corresponding state
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        // if (name === 'sortBy') setSortBy(value);
        // else if (name === 'order') setOrder(value);
        if (name === 'source') setSource(value);
        
        // else if (name === 'author') setAuthor(value);
        // else if (name === 'date') setDate(value);
        // fetchReports();
    };

    // Trigger a filter update when the user clicks the "Apply Filter" button
    // const handleFilterClick = () => {
    //     // setReports([]);
    //     // navigate("/news?page=1");
    //     // Update searchParams when user clicks "Apply Filter"
    //     setSearchParams({
    //         page: 1,
    //         // sortBy: sortBy,
    //         // order: order,
    //         source: source,
    //         // author: author,
    //         // date: date,
    //     });
       
    //     // const params = {
    //     //     page: 1,
    //     //     size: itemsPerPage,
    //     //     sortBy: sortBy,
    //     //     order: order,
    //     //     source: source,
    //     //     author: author,
    //     //     date: date,
    //     // };
    //     // try {
    //     //     const response = axios.get(`https://api.wildwareness.net/news`, { params });
    //     //     setReports(response.data.incidents); // Update reports to the filtered results
    //     //     setTotalPages(response.data.pagination.total_pages);
    //     //     setTotalItems(response.data.pagination.total_items);
    //     //     setItemsPerPage(response.data.pagination.size);
    //     // } catch (error) {
    //     //     console.error("Error fetching news reports:", error);
    //     //     setError(error);
    //     // }
    // };

    return (
        <div className="container">
            <h2 className="text-center my-4">News Reports</h2>

            {/* Filter Inputs */}
            {/* <div className="form-group me-2">
                <label>Source: </label>
                <input
                    type="text"
                    name="source"
                    value={source}
                    onChange={handleFilterChange}
                    className="form-control form-control-sm"
                    placeholder="Filter by source"
                />
            </div> */}

            <div className="form-group me-2">
                <label>Source: </label>
                <select name="source" value={source} onChange={handleFilterChange} className="form-control form-control-sm">
                    <option value="india.com">india.com</option>
                    <option value="date">Date</option>
                </select>
            </div>
{/* 
            <div className="form-group me-2">
                <label>Author: </label>
                <input
                    type="text"
                    name="author"
                    value={author}
                    placeholder="Filter by author"
                    onChange={handleFilterChange}
                    className="form-control form-control-sm"
                />
            </div>

            <div className="form-group me-2">
                <label>Date: </label>
                <input
                    type="text"
                    name="date"
                    value={date}
                    placeholder="Filter by date"
                    onChange={handleFilterChange}
                    className="form-control form-control-sm"
                />
            </div>

            <div className="form-group me-2">
                <label>Sort By: </label>
                <select name="sortBy" value={sortBy} onChange={handleFilterChange} className="form-control form-control-sm">
                    <option value="title">Title</option>
                    <option value="date">Date</option>
                </select>
            </div>

            <div className="form-group me-2">
                <label>Order: </label>
                <select name="order" value={order} onChange={handleFilterChange} className="form-control form-control-sm">
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>
            </div> */}

            {/* Apply Filter Button */}
            {/* <button onClick={handleFilterClick} className="btn btn-primary my-3">
                Apply Filter
            </button> */}

            {/* Loading Indicator */}
            {loading && <p className="text-center">Loading...</p>}

            {/* Render the Reports */}
            <div className="row">
                {reports.length > 0 ? (
                    reports.map((report) => (
                        <div key={report.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={report.image_url} alt={report.title}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Title:</strong> <span className="card-title">{report.title}</span></li>
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
                    !loading && <p className="text-center">No reports found matching your filter criteria.</p>
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
