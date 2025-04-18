import { useState, useEffect } from 'react';
import axios from 'axios';
import {useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import Select from 'react-select';
import { highlightText } from './GeneralSearchPage';
import ReportCard from '../components/ReportCard';

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
    const [sort_by, setSortBy] = useState('');
    const [order, setOrder] = useState('');
    const [source, setSource] = useState('');
    const [author, setAuthor] = useState('');
    const [date, setDate] = useState('');
    const [categories, setCategories] = useState([]);

    const categoryOptions = [
        'general', 'business', 'politics', 'food', 'health', 
        'travel', 'sports', 'tech', 'science'
    ].map(cat => ({ value: cat, label: cat }));

    useEffect(() => {
        const queryParams = new URLSearchParams(query.search);
        const pageParam = parseInt(queryParams.get('page'));
        const resolvedPage = !isNaN(pageParam) && pageParam > 0 ? pageParam : 1;

        const fetchReports = async () => {
            try {
                setLoading("Loading...");

                const baseURL = `http://localhost:3000/news`;
                const categoryValues = categories.map(c => c.value).join(',');
                const url = `${baseURL}?page=${resolvedPage}&size=${itemsPerPage}&search=${search_text}&sort_by=${sort_by}&order=${order}&source=${source}&author=${author}&date=${date}&categories=${categoryValues}`;
                const response = await axios.get(url);
                setReports(response.data.reports);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);

                if (resolvedPage !== currentPage) {
                    setCurrentPage(resolvedPage);
                }

                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
            } catch (error) {
                console.error("Error fetching news reports:", error);
            }
        };

        fetchReports();
    }, [query.search, search_text, itemsPerPage, sort_by, order, author, source, categories, date]);

    const handlePageChange = (page) => {
        if (page !== currentPage) {
            navigate(`/news?page=${page}`);
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        }
    };

    const updateSearchInput = (event) => {
        setSearchText(event.target.value);
        navigate(`/news?page=1`);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'source') setSource(value);
        else if (name === 'author') setAuthor(value);
        else if (name === 'date') setDate(value);
        else if (name === 'sort_by') setSortBy(value);
        else if (name === 'order') setOrder(value);
        navigate(`/news?page=1`);
    };

    const handleCategoryChange = (selectedOptions) => {
        setCategories(selectedOptions || []);
        navigate(`/news?page=1`);
    };

    // Clear all filters
    const clearAllFilters = () => {
        setSortBy('');
        setOrder('');
        setSource('');
        setAuthor('');
        setDate('');
        setCategories([]);
        setSearchText('');
        navigate(`/news?page=1`);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">News Reports</h2>

            <div className="d-flex flex-wrap align-items-center justify-content-center mb-4 gap-3">
                <div className="form-group me-2">
                    <label>Sort By:</label>
                    <select name="sort_by" value={sort_by} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">Select</option>
                        <option value="title">Title</option>
                        <option value="source">Source</option>
                        <option value="author">Author</option>
                        <option value="published_at">Date</option>
                    </select>
                </div>
                <div className="form-group me-2">
                    <label>Order:</label>
                    <select name="order" value={order} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">Select</option>
                        <option value="asc">Ascending</option>
                        <option value="desc">Descending</option>
                    </select>
                </div>
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
            {/* Search Bar and Clear All Filters Button */}
            <div className="d-flex justify-content-center mb-4">
                <div className="w-100 px-3" style={{ maxWidth: '700px' }}>
                    <form className="d-flex flex-column flex-sm-row" role="search" onSubmit={(e) => e.preventDefault()}>
                    <input
                        className="form-control me-sm-2 mb-2 mb-sm-0"
                        type="search"
                        placeholder="Search"
                        aria-label="Search"
                        value={search_text}
                        onChange={updateSearchInput}
                    />
                    <button className="btn btn-primary" style={{minWidth: '100px'}}
                        onClick={clearAllFilters}
                    >
                        Clear All
                    </button>
                    </form>
                </div>
            </div>

            <div className="row">
                {reports.length > 0 ? (
                    reports.map((report) => (
                        <ReportCard
                        report={report}
                        search_text={search_text}
                        highlightText={highlightText}
                    />
                    ))
                ) : (
                    <p className="text-center">{loading}</p>
                )}
            </div>
            {/* Result count */}
            {totalItems > 0 && (
                <p className="text-muted text-start ms-2 text-center">
                    Showing report <strong>{((currentPage - 1) * itemsPerPage) + 1} – {Math.min(currentPage * itemsPerPage, totalItems)} </strong> out of <strong>{totalItems}</strong>
                </p>
            )}
            {/* Pagination */}
            <div className="d-flex justify-content-center mt-4">
                <Pagination
                    totalPages={totalPages}
                    currentPage={currentPage}
                    onPageChange={handlePageChange}
                />
            </div>
        </div>
    );
}

export default NewsReports;
