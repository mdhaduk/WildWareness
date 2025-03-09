import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import Pagination from '../components/Pagination';

function Shelters() {
    const [shelters, setshelters] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchParams, setSearchParams] = useSearchParams();

    // Extract page parameter from URL
    const pageParam = parseInt(searchParams.get("page")) || 1;

    useEffect(() => {
        const fetchshelters = async () => {
            try {
                console.log("Fetching data for page:", pageParam);
                const response = await axios.get(`http://127.0.0.1:5000/shelters`, {
                    params: { page: pageParam, size: itemsPerPage },
                });

                console.log(response.data); // Debugging
                setshelters(response.data.shelters);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setItemsPerPage(response.data.pagination.size);
            } catch (error) {
                console.error("Error fetching shelter instances:", error);
            }
        };

        fetchshelters();
    }, [pageParam]); // ✅ Correct dependency to avoid infinite loops

    const handlePageChange = (page) => {
        // Update the URL and trigger a re-render
        setSearchParams({ page });
    };

    return (
        <div className="container">
            <h2 className="text-center my-4">Shelters</h2>

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
