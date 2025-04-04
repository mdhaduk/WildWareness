import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import { highlightText } from './GeneralSearchPage';

function Wildfires() {
    const [wildfires, setWildfires] = useState([]);
    const [totalPages, setTotalPages] = useState();
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState();
    const [search_text, setSearchText] = useState('');
    const [loading, setLoading] = useState('');
    const [availableLocations, setAvailableLocations] = useState([]);

    const itemsPerPage = 9;
    const query = useLocation();
    const navigate = useNavigate();

    // Filters and sorting state
    const [sortBy, setSortBy] = useState('county');
    const [order, setOrder] = useState('asc');
    const [location, setLocation] = useState('');
    const [year, setYear] = useState('');
    const [acres_burned, setAcresBurned] = useState('');

    useEffect(() => {
        const fetchWildfires = async () => {
            try {
                const queryParams = new URLSearchParams(query.search);
                const pageParam = queryParams.get('page');
                const passedPageParam = pageParam ? parseInt(pageParam, 10) : 1;

                setLoading("Loading...");

                const baseURL = `https://api.wildwareness.net/wildfire_incidents`;
                const url = search_text.trim()
                    ? `${baseURL}?page=${passedPageParam}&size=${itemsPerPage}&search=${search_text}&sort_by=${sortBy}&order=${order}&location=${location}&year=${year}&acres_burned=${acres_burned}`
                    : `${baseURL}?page=${passedPageParam}&size=${itemsPerPage}&sort_by=${sortBy}&order=${order}&location=${location}&year=${year}&acres_burned=${acres_burned}`;

                const response = await axios.get(url);

                setWildfires(response.data.incidents);
                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setCurrentPage(response.data.pagination.page);
            } catch (error) {
                console.error("Error fetching wildfire instances:", error);
                setLoading("Error fetching data.");
            }
        };

        fetchWildfires();
    }, [search_text, currentPage, itemsPerPage, sortBy, order, location, year, acres_burned]);

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
        setCurrentPage(page);
        navigate(`/incidents?page=${page}`);
    };

    const updateSearchInput = (event) => {
        console.log("SEARCH TEXT: " + event.target.value)
        setSearchText(event.target.value);
        handlePageChange(1);
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        if (name === 'sortBy') setSortBy(value);
        else if (name === 'order') setOrder(value);
        else if (name === 'location') setLocation(value);
        else if (name === 'year') setYear(value);
        else if (name === 'acres_burned') setAcresBurned(value);
        handlePageChange(1);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Wildfire Incidents</h2>

            {/* Filter and sorting controls */}
            <div className="d-flex flex-wrap align-items-center justify-content-center mb-4">
                <div className="form-group me-2">
                    <label>Sort By:</label>
                    <select name="sortBy" value={sortBy} onChange={handleFilterChange} className="form-select form-select-sm">
                        <option value="name">Name</option>
                        <option value="county">County</option>
                    </select>
                </div>

                <div className="form-group me-2">
                    <label>Order:</label>
                    <select name="order" value={order} onChange={handleFilterChange} className="form-select form-select-sm">
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
            </div>

            {/* Search Bar */}
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

            {/* Wildfire Cards */}
            <div className="row">
                {wildfires.length > 0 ? (
                    wildfires.map((wildfire) => (
                        <div key={wildfire.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={wildfire.url || "default-image.jpg"} alt={wildfire.name} />
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {highlightText(wildfire.name, search_text)}</li>
                                    <li className="list-group-item"><strong>County:</strong> {highlightText(wildfire.county, search_text)}</li>
                                    <li className="list-group-item"><strong>Location:</strong> {highlightText(wildfire.location, search_text)}</li>
                                    <li className="list-group-item"><strong>Year:</strong> {highlightText(wildfire.year, search_text)}</li>
                                    <li className="list-group-item"><strong>Acres Burned:</strong> {highlightText(wildfire.acres_burned, search_text)}</li>
                                    <li className="list-group-item"><strong>Status:</strong> {highlightText(wildfire.status, search_text)}</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/incidents/${wildfire.id}`} className="btn btn-primary">Read More</Link>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className='text-center'>{loading}</p>
                )}
            </div>

            {/* Pagination */}
            <div className="d-flex mt-4">
                <Pagination 
                    totalPages={totalPages} 
                    currentPage={currentPage} 
                    onPageChange={handlePageChange}  
                    totalItems={totalItems} 
                    itemsPerPage={itemsPerPage} 
                    url={'/incidents'}
                />
            </div>
        </div>
    );
}

export default Wildfires;
