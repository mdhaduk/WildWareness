import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Pagination from '../components/Pagination';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const escapeRegExp = (string) => {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // Escapes special characters
};

export const highlightText = (text, search) => {
    if (!search) return text;

    // Escape special characters in each search word
    const searchWords = search.split(/\s+/).filter(Boolean).map(escapeRegExp);
    const regex = new RegExp(`(${searchWords.join('|')})`, 'gi'); // Create regex with escaped words

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
    const [loading, setLoading] = useState("No results found");
    const itemsPerPage = 9;

    const search = async () => {
        try {
            if (!search_input.trim()) { // Guard against empty searches
                return;
            }
            setLoading("Loading...");
            const response = await axios.get(`http://localhost:3000/search?text=${search_input}&page=${currentPage}`);
            setResults(response.data.results);
            setTotalPages(response.data.pagination.total_pages);
            setTotalItems(response.data.pagination.total_items);
            setLoading("No results found")
        } catch (error) {
            console.error("Error fetching search results:", error);
        }
    };

    const updateSearchInput = (event) => {
        setSearchInput(event.target.value);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
        setResults([]);
    };

    useEffect(() => {
        search();
    }, [currentPage]);

    const determineIdentity = (card) => {
        if (card.identity === 'wildfire') {
            return (
                <div key={card.id} className="col">
                    <div className="card" style={{ width: '22rem' }}>
                        <img
                            src={card.thumbnail_URL}
                            style={{ height: '200px', objectFit: 'cover' }}
                            className="card-img-top"
                            alt={card.name}
                        />
                        <ul className="list-group list-group-flush">
                            <li className="list-group-item text-truncate">
                                <strong>Name:</strong> {highlightText(card.name, search_input)}
                            </li>
                            <li className="list-group-item text-truncate">
                                <strong>County:</strong> {highlightText(card.county, search_input)}
                            </li>
                            <li className="list-group-item text-truncate">
                                <strong>Location:</strong> {highlightText(card.location, search_input)}
                            </li>
                            <li className="list-group-item text-truncate">
                                <strong>Year:</strong> {highlightText(card.year, search_input)}
                            </li>
                            <li className="list-group-item text-truncate">
                                <strong>Acres Burned:</strong> {highlightText(card.acres_burned, search_input)}
                            </li>
                            <li className="list-group-item text-truncate">
                                <strong>Status:</strong> {highlightText(card.status, search_input)}
                            </li>
                        </ul>
                        <div className="card-body">
                            <Link to={`/incidents/${card.id}`} state={{ searchTerm: search_input }} className="card-link">
                                Read More
                            </Link>
                        </div>
                    </div>
                </div>
            );
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
                        value={search_text}
                        onChange={updateSearchInput}
                    />
                </form>
            </div>
            {/* All Cards */}
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
            <div className="d-flex justify-content-center mt-4">
                <Pagination
                    totalPages={totalPages}
                    currentPage={currentPage}
                    onPageChange={handlePageChange}
                    totalItems={totalItems}
                    itemsPerPage={itemsPerPage}
                    url={'/search'}
                />
            </div>
        </div>
    );
};

export default GeneralSearchPage;
