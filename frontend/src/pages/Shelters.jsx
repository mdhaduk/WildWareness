import { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import { highlightText } from './GeneralSearchPage';
import ShelterCard from '../components/ShelterCard';

function Shelters() {
    const [shelters, setShelters] = useState([]);
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
    const [county, setCounty] = useState('');
    const [zipCode, setZipCode] = useState('');
    const [phone, setPhone] = useState('');
    const [rating, setRating] = useState('');

    useEffect(() => {
        const queryParams = new URLSearchParams(query.search);
        const pageParam = parseInt(queryParams.get('page'), 10);
        const resolvedPage = !isNaN(pageParam) && pageParam > 0 ? pageParam : 1;

        const fetchShelters = async () => {
            try {
                setLoading("Loading...");
                const baseURL = `https://api.wildwareness.net/shelters`;

                const url = `${baseURL}?page=${resolvedPage}&size=${itemsPerPage}&search=${search_text}&sort_by=${sortBy}&order=${order}&county=${county}&zipCode=${zipCode}&phone=${phone}&rating=${rating}`;
                const response = await axios.get(url);

                setShelters(response.data.shelters);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);

                if (resolvedPage !== currentPage) {
                    setCurrentPage(resolvedPage);
                }

                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
            } catch (error) {
                console.error("Error fetching shelter instances:", error);
                setLoading("Error fetching data.");
            }
        };

        fetchShelters();
    }, [query.search, search_text, itemsPerPage, sortBy, order, county, zipCode, phone, rating]);

    useEffect(() => {
        const fetchLocations = async () => {
            try {
                const res = await axios.get("https://api.wildwareness.net/shelter_locations");
                setAvailableLocations(res.data.locations || []);
            } catch (error) {
                console.error("Error loading locations:", error);
            }
        };

        fetchLocations();
    }, []);

    const handlePageChange = (page) => {
        if (page !== currentPage) {
            navigate(`/shelters?page=${page}`);
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        }
    };

    const updateSearchInput = (event) => {
        setSearchText(event.target.value);
        navigate(`/shelters?page=1`);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'sortBy') setSortBy(value);
        else if (name === 'order') setOrder(value);
        else if (name === 'county') setCounty(value);
        else if (name === 'zipCode') setZipCode(value);
        else if (name === 'phone') setPhone(value);
        else if (name === 'rating') setRating(value);
        navigate(`/shelters?page=1`);
    };

    // Clear all filters
    const clearAllFilters = () => {
        setSortBy('');
        setOrder('');
        setCounty('');
        setZipCode('');
        setPhone('');
        setRating('');
        setSearchText('');
        navigate(`/shelters?page=1`);
    };
    

    return (
        <div className="container">
            <h2 className="text-center my-4">Shelters</h2>

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
                    <label>County:</label>
                    <select name="county" value={county} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="">All</option>
                        {availableLocations.map((loc) => (
                            <option key={loc} value={loc}>{loc}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group me-2">
                    <label>Zip Code:</label>
                    <input
                        type="text"
                        name="zipCode"
                        value={zipCode}
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                        placeholder="Enter Zip Code"
                    />
                </div>

                <div className="form-group me-2">
                    <label>Phone Area Code:</label>
                    <input
                        type="text"
                        name="phone"
                        value={phone}
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                        placeholder="Enter Area Code"
                    />
                </div>

                <div className="form-group me-2">
                    <label>Rating:</label>
                    <input
                        type="text"
                        name="rating"
                        value={rating}
                        onChange={handleFilterChange}
                        className="form-control form-control-sm"
                        placeholder="Enter Rating"
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

            {/* Shelter Cards */}
            <div className="row">
                {shelters.length > 0 ? (
                    shelters.map((shelter) => (
                    <ShelterCard
                        shelter={shelter}
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
                    Showing shelter <strong>{((currentPage - 1) * itemsPerPage) + 1} – {Math.min(currentPage * itemsPerPage, totalItems)} </strong> out of <strong>{totalItems}</strong>
                </p>
            )}
            {/* Pagination */}
            <div className="d-flex justify-content-center mt-4">
                <Pagination 
                    totalPages={totalPages} 
                    currentPage={currentPage} 
                    onPageChange={handlePageChange}  
                    totalItems={totalItems} 
                    itemsPerPage={itemsPerPage} 
                    url={'/shelters'}
                />
            </div>
        </div>
    );
}

export default Shelters;
