import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import Pagination from '../components/Pagination';

function Shelters() {
    const [shelters, setShelters] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchParams, setSearchParams] = useSearchParams();
    const [maxOccupancy, setMaxOccupancy] = useState('');
    const [isFilterVisible, setIsFilterVisible] = useState(false);

    // Extract page parameter from URL
    const pageParam = parseInt(searchParams.get("page")) || 1;
    const maxOccupancyParam = searchParams.get("max_occupancy");

    useEffect(() => {
        // Set initial value from URL if present
        if (maxOccupancyParam) {
            setMaxOccupancy(maxOccupancyParam);
        }
    }, [maxOccupancyParam]);

    useEffect(() => {
        const fetchShelters = async () => {
            try {
                console.log("Fetching data for page:", pageParam);
                // Build params object
                const params = { 
                    page: pageParam, 
                    size: itemsPerPage 
                };
                
                // Add max_occupancy to params if it exists
                if (maxOccupancy) {
                    params.max_occupancy = maxOccupancy;
                }
                
                const response = await axios.get(`http://127.0.0.1:5000/shelters`, {
                    params: params,
                });

                console.log(response.data); // Debugging
                setShelters(response.data.shelters);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setItemsPerPage(response.data.pagination.size);
            } catch (error) {
                console.error("Error fetching shelter instances:", error);
            }
        };

        fetchShelters();
    }, [pageParam, maxOccupancy]); // Add maxOccupancy as a dependency

    const handlePageChange = (page) => {
        // Update the URL and trigger a re-render
        const newParams = { page };
        if (maxOccupancy) {
            newParams.max_occupancy = maxOccupancy;
        }
        setSearchParams(newParams);
    };

    const handleFilterApply = () => {
        // Reset to page 1 when applying filter
        const newParams = { page: 1 };
        if (maxOccupancy) {
            newParams.max_occupancy = maxOccupancy;
        }
        setSearchParams(newParams);
    };

    const clearFilters = () => {
        setMaxOccupancy('');
        setSearchParams({ page: 1 });
    };

    const toggleFilterVisibility = () => {
        setIsFilterVisible(!isFilterVisible);
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Shelters</h2>

            {/* Filter Section */}
            <div className="mb-4">
                <button 
                    className="btn btn-outline-primary mb-2" 
                    onClick={toggleFilterVisibility}
                >
                    {isFilterVisible ? 'Hide Filters' : 'Show Filters'}
                </button>
                
                {isFilterVisible && (
                    <div className="card p-3">
                        <div className="mb-3">
                            <label htmlFor="maxOccupancy" className="form-label">
                                Maximum Occupancy (or less):
                            </label>
                            <input
                                type="number"
                                className="form-control"
                                id="maxOccupancy"
                                value={maxOccupancy}
                                onChange={(e) => setMaxOccupancy(e.target.value)}
                                placeholder="Enter maximum occupancy"
                                min="1"
                            />
                        </div>
                        <div className="d-flex gap-2">
                            <button 
                                className="btn btn-primary" 
                                onClick={handleFilterApply}
                            >
                                Apply Filters
                            </button>
                            <button 
                                className="btn btn-secondary" 
                                onClick={clearFilters}
                            >
                                Clear Filters
                            </button>
                        </div>
                    </div>
                )}
            </div>

            {/* Active Filters Display */}
            {maxOccupancy && (
                <div className="mb-3">
                    <span className="badge bg-info text-dark me-2">
                        Max Occupancy: {maxOccupancy} or less
                        <button 
                            className="btn-close ms-2" 
                            style={{ fontSize: '0.5rem' }} 
                            onClick={() => {
                                setMaxOccupancy('');
                                const newParams = { ...Object.fromEntries(searchParams.entries()) };
                                delete newParams.max_occupancy;
                                setSearchParams(newParams);
                            }}
                        ></button>
                    </span>
                </div>
            )}

            <div className="row">
                {shelters.length > 0 ? (
                    shelters.map((shelter) => (
                        <div key={shelter.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={shelter.imageUrl || "default-image.jpg"} alt={shelter.name}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {shelter.name}</li>
                                    <li className="list-group-item"><strong>Address:</strong> {shelter.address}</li>
                                    <li className="list-group-item"><strong>Phone:</strong> {shelter.phone}</li>
                                    <li className="list-group-item"><strong>Website:</strong><a href='shelter.website'> {shelter.website}</a></li>
                                    <li className="list-group-item"><strong>Rating:</strong> {shelter.rating}/5</li>
                                    <li className="list-group-item"><strong>County:</strong> {shelter.county || "N/A"}</li>
                                    {shelter.max_occupancy && (
                                        <li className="list-group-item"><strong>Max Occupancy:</strong> {shelter.max_occupancy}</li>
                                    )}
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/shelters/${shelter.id}`} className="btn btn-primary">Read More</Link>
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
                    url={'/shelters'}
                />
            </div>
        </div>
    );
}

export default Shelters;
