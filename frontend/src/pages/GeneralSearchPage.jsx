import 'bootstrap/dist/css/bootstrap.min.css';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Pagination from '../components/Pagination';

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
        
        const search = async () => {
            try {
                setLoading("Loading...");
                const response = await axios.get(`https://api.wildwareness.net/search?text=${search_input}&page=${resolvedPage}&size=${itemsPerPage}`);
                setResults(response.data.instances);
                setTotalPages(response.data.pagination.total_pages);
                setTotalItems(response.data.pagination.total_items);
    
                if (response.data.pagination.total_items === 0) {
                    setLoading("No Results");
                }
            } catch (error) {
                console.error("Error fetching search results:", error);
                setLoading("Error fetching results.");
            }
        };
    
        search();
    }, [search_input, query.search, currentPage]);

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
    const determineIdentity = (card) => {
        let identity = '';
        if ('acres_burned' in card && 'status' in card) {
            identity = 'wildfire';
        } else if ('address' in card && 'phone' in card) {
            identity = 'shelter';
        } else if ('title' in card && 'published_at' in card) {
            identity = 'report';
        } else {
            console.warn('Unknown card type:', card);
            return null;
        }

        const cardImg = (
            <img
                src={card.image_url || card.url || card.imageUrl}
                className="card-img"
                alt={card.name || card.title}
            />
        );

        const baseCard = (body, linkPath) => (
            <div key={card.id} className="col-md-4 mb-4">
                <div className="card" style={{ width: '22rem' }}>
                    {cardImg}
                    <ul className="list-group list-group-flush">{body}</ul>
                    <div className="card-body text-center">
                        <Link to={linkPath} state={{ searchTerm: search_input }} className="card-link">
                            Read More
                        </Link>
                    </div>
                </div>
            </div>
        );

        if (identity === 'wildfire') {
            return baseCard([
                <li key="name" className="list-group-item text-truncate"><strong>Name:</strong> {highlightText(card.name, search_input)}</li>,
                <li key="county" className="list-group-item text-truncate"><strong>County:</strong> {highlightText(card.county, search_input)}</li>,
                <li key="location" className="list-group-item text-truncate"><strong>Location:</strong> {highlightText(card.location, search_input)}</li>,
                <li key="year" className="list-group-item text-truncate"><strong>Year:</strong> {highlightText(card.year, search_input)}</li>,
                <li key="acres" className="list-group-item text-truncate"><strong>Acres Burned:</strong> {highlightText(card.acres_burned, search_input)}</li>,
                <li key="status" className="list-group-item text-truncate"><strong>Status:</strong> {highlightText(card.status, search_input)}</li>,
            ], `/incidents/${card.id}`);
        }

        if (identity === 'shelter') {
            return baseCard([
                <li key="name" className="list-group-item text-truncate"><strong>Name:</strong> {highlightText(card.name, search_input)}</li>,
                <li key="county" className="list-group-item text-truncate"><strong>County:</strong> {highlightText(card.county, search_input)}</li>,
                <li key="address" className="list-group-item text-truncate"><strong>Address:</strong> {highlightText(card.address, search_input)}</li>,
                <li key="phone" className="list-group-item text-truncate"><strong>Phone:</strong> {highlightText(card.phone, search_input)}</li>,
                <li key="rating" className="list-group-item text-truncate"><strong>Rating:</strong> {highlightText(card.rating, search_input)}</li>,
            ], `/shelters/${card.id}`);
        }

        if (identity === 'report') {
            return baseCard([
                <li key="title" className="list-group-item text-truncate"><strong>Title:</strong> <span className='card-title'>{highlightText(report.title, search_text)}</span></li>,
                <li key="source" className="list-group-item text-truncate"><strong>Source:</strong> {highlightText(card.source, search_input)}</li>,
                <li key="date" className="list-group-item text-truncate"><strong>Date:</strong> {highlightText(card.published_at, search_input)}</li>,
                <li key="author" className="list-group-item text-truncate"><strong>Author:</strong> {highlightText(card.author, search_input)}</li>,
                <li key="categories" className="list-group-item text-truncate"><strong>Categories:</strong> {highlightText(card.categories, search_input)}</li>,
            ], `/news/${card.id}`);
        }
    };

    return (
        <div className="container text-center">
            <h1>Search</h1>
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
                {search_input.trim() && results.length > 0 ? results.map((result) => determineIdentity(result)).filter(Boolean) : <p>{loading}</p>}
            </div>
            <div>
                {search_input.trim() && totalItems > 0 && (
                        <p className="text-muted text-start ms-2 text-center">
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
