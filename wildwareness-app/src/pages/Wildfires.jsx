import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import Pagination from '../components/Pagination';

function WildfireIncidentsPage() {
    const [wildfires, setWildfires] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchParams, setSearchParams] = useSearchParams();

    // Extract page parameter from URL
    const pageParam = parseInt(searchParams.get("page")) || 1;

    useEffect(() => {
        const fetchWildfires = async () => {
            try {
                console.log("Fetching data for page:", pageParam);
                const response = await axios.get(`http://127.0.0.1:5000/wildfire_incidents`, {
                    params: { page: pageParam, size: itemsPerPage },
                });

                console.log(response.data); // Debugging
                setWildfires(response.data.incidents);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setItemsPerPage(response.data.pagination.size);
            } catch (error) {
                console.error("Error fetching wildfire instances:", error);
            }
        };

        fetchWildfires();
    }, [pageParam]); // ✅ Correct dependency to avoid infinite loops

    const handlePageChange = (page) => {
        // Update the URL and trigger a re-render
        setSearchParams({ page });
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Wildfire Incidents</h2>

            <div className="row">
                {wildfires.length > 0 ? (
                    wildfires.map((wildfire) => (
                        <div key={wildfire.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={wildfire.url || "default-image.jpg"} alt={wildfire.name}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {wildfire.name}</li>
                                    <li className="list-group-item"><strong>County:</strong> {wildfire.county}</li>
                                    <li className="list-group-item"><strong>Location:</strong> {wildfire.location}</li>
                                    <li className="list-group-item"><strong>Year:</strong> {wildfire.year}</li>
                                    <li className="list-group-item"><strong>Acres Burned:</strong> {wildfire.acres_burned}</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/wildfire/${wildfire.id}`} className="btn btn-primary">Read More</Link>
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
                    url={'/incidents'}
                />
            </div>
        </div>
    );
}

export default WildfireIncidentsPage;
