import { useState, useEffect } from 'react';
import axios from 'axios';
import {useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import { highlightText } from './GeneralSearchPage';
import WildfireCard from '../components/WildfireCard';

function Wildfires() {
    const [wildfires, setWildfires] = useState([]);
    const [totalPages, setTotalPages] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState();
    const [search_text, setSearchText] = useState('');
    const [loading, setLoading] = useState('');
    const [availableLocations, setAvailableLocations] = useState([]);

    const itemsPerPage = 9;
    const query = useLocation();
    const navigate = useNavigate();

    // Filters and sorting state
    const [sortBy, setSortBy] = useState('');
    const [order, setOrder] = useState('');
    const [location, setLocation] = useState('');
    const [year, setYear] = useState('');
    const [acres_burned, setAcresBurned] = useState('');
    const [status, setStatus] = useState('');

    useEffect(() => {
        const queryParams = new URLSearchParams(query.search);
        const pageParam = parseInt(queryParams.get('page'), 10);
        const resolvedPage = !isNaN(pageParam) && pageParam > 0 ? pageParam : 1;

        const fetchWildfires = async () => {
            try {
                setLoading("Loading...");

                const baseURL = `https://api.wildwareness.net/wildfire_incidents`;
                const url = `${baseURL}?page=${resolvedPage}&size=${itemsPerPage}&search=${search_text}&sort_by=${sortBy}&order=${order}&location=${location}&year=${year}&acres_burned=${acres_burned}&status=${status}`;

                const response = await axios.get(url);

                setWildfires(response.data.incidents);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);

                if (resolvedPage !== currentPage) {
                    setCurrentPage(resolvedPage);
                }

                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
            } catch (error) {
                console.error("Error fetching wildfire instances:", error);
                setLoading("Error fetching data.");
            }
        };

        fetchWildfires();
    }, [query.search, search_text, itemsPerPage, sortBy, order, location, year, acres_burned, status]);

    useEffect(() => {
        const fetchLocations = async () => {
            try {
                const res = await axios.get("https://api.wildwareness.net/wildfire_locations");
                setAvailableLocations(res.data.locations || []);
            } catch (error) {
                console.error("Error loading locations:", error);
            }
        };

        fetchLocations();
    }, []);

    const handlePageChange = (page) => {
        if (page !== currentPage) {
            navigate(`/incidents?page=${page}`);
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        }
    };

    const updateSearchInput = (event) => {
        setSearchText(event.target.value);
        navigate(`/incidents?page=1`);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'sortBy') setSortBy(value);
        else if (name === 'order') setOrder(value);
        else if (name === 'location') setLocation(value);
        else if (name === 'year') setYear(value);
        else if (name === 'acres_burned') setAcresBurned(value);
        else if (name === 'status') setStatus(value);
        navigate(`/incidents?page=1`);
    };

    const clearAllFilters = () => {
        setSortBy('');
        setOrder('');
        setLocation('');
        setYear('');
        setAcresBurned('');
        setStatus('');
        setSearchText('');
        navigate(`/incidents?page=1`);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Wildfire Incidents</h2>

            {/* Filter and sorting controls */}
            <div className="d-flex flex-wrap align-items-center justify-content-center mb-4">
                <div className="form-group me-2">
                    <label>Sort By:</label>
                    <select name="sortBy" value={sortBy} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">Select</option>
                        <option value="name">Name</option>
                        <option value="county">County</option>
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
                    <label>Location:</label>
                    <select name="location" value={location} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">All</option>
                        {availableLocations.map((loc) => (
                            <option key={loc} value={loc}>{loc}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group me-2">
                    <label>Year:</label>
                    <input
                        type="text"
                        name="year"
                        value={year}
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                        placeholder="Enter Year"
                    />
                </div>

                <div className="form-group me-2">
                    <label>Acres Burned:</label>
                    <select name="acres_burned" value={acres_burned} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">All</option>
                        <option value="500">{">"}500</option>
                        <option value="1000">{">"}1000</option>
                        <option value="2000">{">"}2000</option>
                        <option value="4000">{">"}4000</option>
                        <option value="8000">{">"}8000</option>
                        <option value="16000">{">"}16000</option>
                        <option value="32000">{">"}32000</option>
                        <option value="64000">{">"}64000</option>
                    </select>
                </div>

                <div className="form-group me-2">
                    <label>Status:</label>
                    <select name="status" value={status} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">All</option>
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                    </select>
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

            {/* Wildfire Cards */}
            <div className="row">
                {wildfires.length > 0 ? (
                    wildfires.map((wildfire) => (
                    <WildfireCard
                        wildfire={wildfire}
                        search_text={search_text}
                        highlightText={highlightText}
                    />
                    ))
                ) : (
                    <p className='text-center'>{loading}</p>
                )}
            </div>
            

            {/* Result count */}
            {totalItems > 0 && (
                <p className="text-muted text-start ms-2 text-center">
                    Showing wildfire <strong>{((currentPage - 1) * itemsPerPage) + 1} – {Math.min(currentPage * itemsPerPage, totalItems)} </strong> out of <strong>{totalItems}</strong>
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

export default Wildfires;
