import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import Select from 'react-select';

function NewsReports() {
    const [reports, setReports] = useState([]);
    const [totalPages, setTotalPages] = useState();
    const [totalItems, setTotalItems] = useState();
    const [currentPage, setCurrentPage] = useState(1);
    const [search_text, setSearchText] = useState('');
    const [loading, setLoading] = useState('');

    const itemsPerPage = 9;
    const query = useLocation();
    const navigate = useNavigate();

    // Filters
    const [sortBy, setSortBy] = useState('title');
    const [order, setOrder] = useState('asc');
    const [source, setSource] = useState('');
    const [author, setAuthor] = useState('');
    const [date, setDate] = useState('');
    const [categories, setCategories] = useState([]);

    const categoryOptions = [
        'general', 'business', 'politics', 'food', 'health', 
        'travel', 'sports', 'tech', 'science'
    ].map(cat => ({ value: cat, label: cat }));

    useEffect(() => {
        const fetchReports = async () => {
            try {
                const queryParams = new URLSearchParams(query.search);
                const pageParam = queryParams.get('page');
                const passedPageParam = pageParam ? parseInt(pageParam, 10) : 1;
                setLoading("Loading...");
                const baseURL = `https://api.wildwareness.net/news`;
                const categoryValues = categories.map(c => c.value).join(',');
                const url = `${baseURL}?page=${passedPageParam}&size=${itemsPerPage}&search=${search_text}&sort_by=${sortBy}&order=${order}&source=${source}&author=${author}&date=${date}&categories=${categoryValues}`;

                const response = await axios.get(url);
                setReports(response.data.reports);
                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setCurrentPage(response.data.pagination.page);
            } catch (error) {
                console.error("Error fetching news reports:", error);
            }
        };

        fetchReports();
    }, [search_text, currentPage, itemsPerPage, sortBy, order, author, source, categories, date]);

    const handlePageChange = (page) => {
        setCurrentPage(page);
        navigate(`/news?page=${page}`);
    };

    const updateSearchInput = (event) => {
        setSearchText(event.target.value);
        handlePageChange(1);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'source') setSource(value);
        else if (name === 'author') setAuthor(value);
        else if (name === 'date') setDate(value);
        else if (name === 'sortBy') setSortBy(value);
        else if (name === 'order') setOrder(value);
        handlePageChange(1);
    };

    const handleCategoryChange = (selectedOptions) => {
        setCategories(selectedOptions || []);
        handlePageChange(1);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">News Reports</h2>
            <div className="d-flex flex-wrap align-items-center justify-content-center mb-4 gap-3">
                <div className="form-group me-2">
                    <label>Source:</label>
                    <input
                        type="text"
                        name="source"
                        value={source}
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                        placeholder="Enter Source"
                    />
                </div>

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
                        type="date"
                        name="date"
                        value={date}
                        placeholder="Filter by date"
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                    />
                </div>

                <div className="form-group me-2" style={{ minWidth: '250px' }}>
                    <label>Categories:</label>
                    <Select
                        isMulti
                        name="categories"
                        options={categoryOptions}
                        value={categories}
                        onChange={handleCategoryChange}
                        className="basic-multi-select"
                        classNamePrefix="select"
                        placeholder="Select categories..."
                    />
                </div>
            </div>

            <div className="container text-center" style={{ width: '50%', margin: '0 auto', marginBottom: '20px' }}>
                <form className="d-flex" role="search" onSubmit={(e) => e.preventDefault()}>
                    <input
                        className="form-control me-2"
                        type="search"
                        placeholder="Search"
                        aria-label="Search"
                        value={search_text}
                        onChange={updateSearchInput}
                    />
                </form>
            </div>

            <div className="row">
                {reports.length > 0 ? (
                    reports.map((report) => (
                        <div key={report.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={report.image_url} alt={report.title} />
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Title:</strong> <span className='card-title'>{highlightText(report.title, search_text)}</span></li>
                                    <li className="list-group-item"><strong>Source:</strong> {highlightText(report.source, search_text)}</li>
                                    <li className="list-group-item"><strong>Date:</strong> {highlightText(report.published_at, search_text)}</li>
                                    <li className="list-group-item"><strong>Author:</strong> {highlightText(report.author, search_text)}</li>
                                    <li className="list-group-item"><strong>Categories:</strong> {highlightText(report.categories, search_text)}</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/news/${report.id}`} className="btn btn-primary">Read More</Link>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-center">{loading}</p>
                )}
            </div>

            {/* Pagination */}
            <div className="d-flex justify-content-center mt-4">
                <Pagination
                    totalPages={totalPages}
                    currentPage={currentPage}
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
