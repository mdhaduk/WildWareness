import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import { highlightText } from './GeneralSearchPage';

function Shelters() {
    const [shelters, setShelters] = useState([]);
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
    const [address, setAddress] = useState('');
    const [rating, setRating] = useState('');

    useEffect(() => {
        const fetchshelters = async () => {
            try {
                const queryParams = new URLSearchParams(query.search);
                const pageParam = queryParams.get('page');
                const passedPageParam = pageParam ? parseInt(pageParam, 10) : 1;
                setLoading("Loading...");
                const baseURL = `https://api.wildwareness.net/shelters`;
                const url = search_text.trim()
                ? `${baseURL}?page=${passedPageParam}&size=${itemsPerPage}&search=${search_text}&sort_by=${sortBy}&order=${order}&address=${address}&rating=${rating}`
                : `${baseURL}?page=${passedPageParam}&size=${itemsPerPage}&sort_by=${sortBy}&order=${order}&address=${address}&rating=${rating}`;
                const response = await axios.get(url)
                setShelters(response.data.shelters);
                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setCurrentPage(response.data.pagination.page);
            } catch (error) {
                console.error("Error fetching shelter instances:", error);
                setLoading("Error fetching data.");
            }
        };

        fetchshelters();
    }, [search_text, currentPage, itemsPerPage, sortBy, order, address, rating]);

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
        setCurrentPage(page);
        navigate(`/shelters?page=${page}`);
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
        else if (name === 'address') setAddress(value);
        else if (name === 'rating') setRating(value);
        handlePageChange(1);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Shelters</h2>


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
                    <label>Address:</label>
                    <select name="address" value={address} onChange={handleFilterChange} className="form-select form-select-sm">
                    <option value="">All</option>
                    {availableLocations.map((loc) => (
                        <option key={loc} value={loc}>{loc}</option>
                    ))}
                    </select>
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

            <div className="row">
                {shelters.length > 0 ? (
                    shelters.map((shelter) => (
                        <div key={shelter.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={shelter.imageUrl || "default-image.jpg"} alt={shelter.name}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {highlightText(shelter.name, search_text)}</li>
                                    <li className="list-group-item"><strong>County:</strong> {highlightText(shelter.county, search_text)}</li>
                                    <li className="list-group-item"><strong>Address:</strong> {highlightText(shelter.address, search_text)}</li>
                                    <li className="list-group-item"><strong>Phone:</strong> {highlightText(shelter.phone, search_text)}</li>
                                    <li className="list-group-item"><strong>Website:</strong><a href={shelter.website}> {highlightText(shelter.website, search_text)}</a></li>
                                    <li className="list-group-item"><strong>Rating:</strong> {highlightText(shelter.rating, search_text)}/5</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/shelters/${shelter.id}`} className="btn btn-primary">Read More</Link>
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
                    url={'/shelters'}
                />
            </div>
        </div>
    );
}

export default Shelters;
