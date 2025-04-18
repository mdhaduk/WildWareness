import { Link } from 'react-router-dom';

const WildfireCard = ({ wildfire, search_text = '', highlightText = (text) => text }) => {
  const {
    id,
    name,
    county,
    location,
    year,
    acres_burned,
    status,
    url, // Image link for wildfire instance
  } = wildfire;

  return (
    <div key={id} className="col-md-4 mb-4">
      <div className="card" style={{ width: '100%' }}>
        <img
          className="card-img"
          src={url}
          onError={(e) => e.target.src = "https://i0.wp.com/calmatters.org/wp-content/uploads/2025/01/010725_Pacific-Palisades-Fire_GETTY_CM_WIDE_01.jpg?fit=2000%2C1125&ssl=1"}
          alt={name}
          style={{ height: '200px', objectFit: 'cover' }}
        />
        <ul className="list-group list-group-flush">
          <li className="list-group-item"><strong>Name:</strong> {highlightText(name, search_text)}</li>
          <li className="list-group-item"><strong>County:</strong> {highlightText(county, search_text)}</li>
          <li className="list-group-item"><strong>Location:</strong> {highlightText(location, search_text)}</li>
          <li className="list-group-item"><strong>Year:</strong> {highlightText(year, search_text)}</li>
          <li className="list-group-item"><strong>Acres Burned:</strong> {highlightText(acres_burned, search_text)}</li>
          <li className="list-group-item"><strong>Status:</strong> {highlightText(status, search_text)}</li>
        </ul>
        <div className="card-body text-center">
          <Link to={`/incidents/${id}`} className="btn btn-primary">Read More</Link>
        </div>
      </div>
    </div>
  );
};

export default WildfireCard;
