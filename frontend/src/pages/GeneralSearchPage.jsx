import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';
import WildfireCard from '../components/WildfireCard';
import ShelterCard from '../components/ShelterCard';
import ReportCard from '../components/ReportCard';

const escapeRegExp = (string) => {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
};

export const highlightText = (text, search) => {
    if (!search) return text;
    const searchWords = search.split(/\s+/).filter(Boolean).map(escapeRegExp);
    const regex = new RegExp(`(${searchWords.join('|')})`, 'gi');
    const words = text.split(regex);
    return words.map((part, index) =>
        searchWords.some(word => part.toLowerCase() === word.toLowerCase()) ? (
            <span key={index} style={{ backgroundColor: 'yellow', fontWeight: 'bold' }}>{part}</span>
        ) : (
            part
        )
    );
};

const GeneralSearchPage = () => {
    const [search_input, setSearchInput] = useState('');
    const [results, setResults] = useState([]);
    const [totalPages, setTotalPages] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const [loading, setLoading] = useState("No results");
    const [isSearching, setisSearching] = useState(false);

    const itemsPerPage = 9;
    const query = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const queryParams = new URLSearchParams(query.search);
        const pageParam = parseInt(queryParams.get('page'), 10);
        const resolvedPage = !isNaN(pageParam) && pageParam > 0 ? pageParam : 1;
        
        if (resolvedPage !== currentPage) {
            setCurrentPage(resolvedPage);
        }
        
        if (!search_input.trim()){
            setResults([]);
            setTotalItems(0);
            setTotalPages(0);
            setLoading("No Results");
            return; 
        }
        
        setisSearching(true);
        const search = async () => {
            try {
                setLoading("Loading...");
                const response = await axios.get(`http://localhost:3000/search?text=${search_input}&page=${resolvedPage}&size=${itemsPerPage}`);
                setResults(response.data.instances);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
                setisSearching(false);
                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
            } catch (error) {
                console.error("Error fetching search results:", error);
                setLoading("Error fetching results.");
            }
        };
        const timer = setTimeout(() => {
            search();
        }, 300);
        return () => {
            clearTimeout(timer);
        };
    }, [search_input, query.search, currentPage, itemsPerPage]);

    const updateSearchInput = (event) => {
        setSearchInput(event.target.value);
        navigate(`/search?page=1`);
    };

    const handlePageChange = (page) => {
        if (page !== currentPage) {
            navigate(`/search?page=${page}`);
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            });
        }
    };
    const categorizeResults = () => {
        const categorized = {
            wildfire: [],
            shelter: [],
            report: [],
        };
    
        results.forEach(result => {
            if ('acres_burned' in result && 'status' in result) {
                categorized.wildfire.push(result);
            } else if ('address' in result && 'phone' in result) {
                categorized.shelter.push(result);
            } else if ('title' in result && 'published_at' in result) {
                categorized.report.push(result);
            }});

            return categorized;
        };

        const categorized = categorizeResults();

    return (
        <div className="container">
            <h1 className="text-center my-4">Search</h1>
            {/* Search Bar */}
            <div className="container text-center" style={{ width: '50%', margin: '0 auto', marginBottom: '20px' }}>
                <form className="d-flex" role="search" onSubmit={(e) => e.preventDefault()}>
                    <input
                        className="form-control me-2"
                        type="search"
                        placeholder="Search"
                        aria-label="Search"
                        value={search_input}
                        onChange={updateSearchInput}
                    />
                </form>
            </div>
            <div className="row gy-4 mt-3">
                {isSearching ? (
                    <div className="text-center mt-4">
                        <p className="text-muted">Loading...</p>
                    </div>
                ) : search_input.trim() && results && results.length > 0 ? (
                    <>
                    {categorized.wildfire.length > 0 && (
                        <div className="mb-5">
                            <h3 className="mb-3 border-bottom pb-2" style={{ color: '#c62828' }}><strong>Wildfire Incidents</strong></h3>
                            <div className="row gy-4">
                                {categorized.wildfire.map((wildfire) => (
                                    <WildfireCard
                                        key={wildfire.id}
                                        wildfire={wildfire}
                                        highlightText={highlightText}
                                        search_text={search_input}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {categorized.shelter.length > 0 && (
                        <div className="mb-5">
                            <h3 className="text-success mb-3 border-bottom pb-2"><strong>Emergency Shelters</strong></h3>
                            <div className="row gy-4">
                                {categorized.shelter.map((shelter) => (
                                    <ShelterCard
                                        key={shelter.id}
                                        shelter={shelter}
                                        highlightText={highlightText}
                                        search_text={search_input}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {categorized.report.length > 0 && (
                        <div className="mb-5">
                            <h3 className="mb-3 border-bottom pb-2" style={{ color: '#003366' }}><strong>Community Reports</strong></h3>
                            <div className="row gy-4">
                                {categorized.report.map((report) => (
                                    <ReportCard
                                        key={report.id}
                                        report={report}
                                        highlightText={highlightText}
                                        search_text={search_input}
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                </>
                ) : (
                    <div className="text-center mt-4">
                        <p className="text-muted">{loading}</p>
                    </div>
                )}
            </div>
            <div>
                {search_input.trim() && totalItems > 0 && (
                        <p className="text-muted text-start ms-2">
                            Showing <strong>{((currentPage - 1) * itemsPerPage) + 1} – {Math.min(currentPage * itemsPerPage, totalItems)} </strong> out of <strong>{totalItems}</strong>
                        </p>
                    ) && 
                    <div className="d-flex justify-content-center mt-4">
                    <Pagination
                        totalPages={totalPages}
                        currentPage={currentPage}
                        onPageChange={handlePageChange}
                    />
                    </div>}
            </div>
        </div>
    );
};

export default GeneralSearchPage;
