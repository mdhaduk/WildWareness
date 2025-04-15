import React from 'react';
import { Link } from 'react-router-dom';

const ReportCard = ({ report, search_text = '', highlightText = (text) => text }) => {
  const {
    id,
    title,
    source,
    published_at,
    author,
    categories,
    image_url, // Image link for report instance
  } = report;

  const imageSrc = image_url || "default-image.jpg";

  return (
    <div key={id} className="col-md-4 mb-4">
      <div className="card" style={{ width: '22rem' }}>
        <img
          className="card-img"
          src={imageSrc}
          onError={(e) => { e.target.src = "default-image.jpg"; }}
          alt={title}
          style={{ objectFit: 'cover' }}
        />
        <ul className="list-group list-group-flush">
            <li className="list-group-item"><strong>Title:</strong> <span className='card-title'>{highlightText(title, search_text)}</span></li>
            <li className="list-group-item"><strong>Source:</strong> {highlightText(source, search_text)}</li>
            <li className="list-group-item"><strong>Date:</strong> {highlightText(published_at, search_text)}</li>
            <li className="list-group-item"><strong>Author:</strong> {highlightText(author, search_text)}</li>
            <li className="list-group-item"><strong>Categories:</strong> {highlightText(categories, search_text)}</li>
        </ul>
        <div className="card-body text-center">
          <Link to={`/news/${id}`} className="btn btn-primary">Read More</Link>
        </div>
      </div>
    </div>
  );
};

export default ReportCard;
