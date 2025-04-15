import React from 'react';
import { Link } from 'react-router-dom';

const ShelterCard = ({ shelter, search_text = '', highlightText = (text) => text }) => {
  const {
    id,
    name,
    county,
    address,
    phone,
    website,
    rating,
    imageUrl, // Image link for shelter instance
  } = shelter;

  const imageSrc = imageUrl || "default-image.jpg";

  return (
    <div key={id} className="col-md-4 mb-4">
      <div className="card" style={{ width: '100%' }}>
        <img
          className="card-img"
          src={imageSrc}
          onError={(e) => { e.target.src = "default-image.jpg"; }}
          alt={name}
          style={{ height: '200px', objectFit: 'cover' }}
        />
        <ul className="list-group list-group-flush">
            <li className="list-group-item"><strong>Name:</strong> {highlightText(name, search_text)}</li>
            <li className="list-group-item"><strong>County:</strong> {highlightText(county, search_text)}</li>
            <li className="list-group-item"><strong>Address:</strong> {highlightText(address, search_text)}</li>
            <li className="list-group-item"><strong>Phone:</strong> {highlightText(phone, search_text)}</li>
            <li className="list-group-item">
                <strong>Website:</strong> <a href={website} target="_blank" rel="noopener noreferrer">{highlightText(website, search_text)}</a>
            </li>
            <li className="list-group-item"><strong>Rating:</strong> {highlightText(rating, search_text)}/5</li>
        </ul>
        <div className="card-body text-center">
          <Link to={`/shelters/${id}`} className="btn btn-primary">Read More</Link>
        </div>
      </div>
    </div>
  );
};

export default ShelterCard;
