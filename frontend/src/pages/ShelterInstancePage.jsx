import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link} from 'react-router-dom';
import axios from 'axios';
import Map from '../components/Map';
import WildfireCard from '../components/WildfireCard';
import ReportCard from '../components/ReportCard';


const ShelterInstancePage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [shelter, setShelter] = useState(null);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    if (!shelter || shelter.id !== id) {
      const fetchShelter = async () => {
        try {
          const response = await axios.get(`https://api.wildwareness.net/shelters/${id}`);
          setShelter(response.data);
        } catch (error) {
          console.error("Error fetching shelter details:", error);
        }
      };
      fetchShelter();
    }
  }, [id]);

  if (!shelter) {
    return <div>Loading...</div>;
  }

  const nearbyWildfires = [];
  for (let i = 0; i < shelter.wildfires.length; i++) {
    nearbyWildfires.push(
      <li key={i}>
            <Link to={`/wildfire_incidents/${shelter.wildfires[i].id}`}>
              {shelter.wildfires[i].name}
            </Link>
      </li>
    );
  }

  const nearbyNewsreports = [];
  for (let i = 0; i < shelter.newsreports.length; i++) {
      nearbyNewsreports.push(
        <li key={i}>
              <Link to={`/news/${shelter.newsreports[i].id}`}>
                {shelter.newsreports[i].name}
              </Link>
        </li>
      );
    }

  const visibleReviews = showAll ? shelter.reviews : shelter.reviews?.slice(0, 2);
  return (
    <div className="container mt-5">
      <h3><strong>{shelter.name}</strong></h3>
      <p>{shelter.address}</p>
      {shelter.website && (
        <a href={shelter.website} target="_blank" rel="noopener noreferrer">{shelter.name}</a>
      )}

      <div className="row my-4 justify-content-center">
        <div className="col-md-8 text-center mb-4">
          <img
            src={shelter.imageUrl || '/default-placeholder.jpg'}
            alt={shelter.name}
            className="img-fluid"
            style={{ height: '300px', width: '600px', objectFit: 'cover' }}
            onError={(e) => { e.target.src = '/default-placeholder.jpg'; }}
          />
        </div>
      </div>

      <div className="container-fluid my-4">
        <h5><strong>Description:</strong></h5>
        <p>{shelter.description || "No description available."}</p>
      </div>

      <Map address={shelter.address} name={shelter.name} />

      <div className="container-fluid my-4">
        <h5><strong>Attributes:</strong></h5>
        <ul className="list-group list-group-flush">
          <li className="list-group-item text-wrap"><strong>Name:</strong> {shelter.name}</li>
          <li className="list-group-item text-wrap"><strong>County:</strong> {shelter.county}</li>
          <li className="list-group-item text-wrap"><strong>Address:</strong> {shelter.address}</li>
          <li className="list-group-item text-wrap"><strong>Phone:</strong> {shelter.phone || "N/A"}</li>
          <li className="list-group-item text-wrap"><strong>Rating:</strong> {shelter.rating ? `${shelter.rating}/5` : "No rating available"}</li>
          <li className="list-group-item text-wrap">
            <strong>Reviews:</strong>
            {visibleReviews && visibleReviews.length > 0 ? (
              <ul>
                {visibleReviews.map((review, index) => (
                  <li key={index} style={{ marginBottom: "10px" }}>{review}</li>
                ))}
              </ul>
            ) : (
              <p>No reviews available.</p>
            )}
            {shelter?.reviews?.length > 2 && (
              <button onClick={() => setShowAll(!showAll)} className="btn btn-link p-0">
                {showAll ? "View Less" : "View More"}
              </button>
            )}
          </li>
        </ul>
      </div>
      <div className="row">
        <h5 className=''><strong>Nearby Wildfires:</strong></h5>
                {shelter.wildfires.length > 0 ? (
                    shelter.wildfires.map((wildfire) => (
                      <WildfireCard
                        key={wildfire.id}
                        wildfire={wildfire}
                        // Optional: pass these only if you want highlighting
                        // search_text={search_text}
                        // highlightText={highlightText}
                      />
                    ))
                ) : (
                    <p className="text-center">Loading...</p>
                )}
        </div>
        <br />
        <div className="row">
        <h5 className=''><strong>Nearby News Reports:</strong></h5>
                {shelter.newsreports.length > 0 ? (
                    shelter.newsreports.map((report) => (
                      <ReportCard
                        key={report.id}
                        report={report}
                        // Optional: pass these only if you want highlighting
                        // search_text={search_text}
                        // highlightText={highlightText}
                      />
                    ))
                ) : (
                    <p className="text-center">Loading...</p>
                )}
        </div>

      <div>
        <button className="btn btn-secondary mb-3" onClick={() => navigate('/shelters')}>Go Back</button>
      </div>
    </div>
  );
};

export default ShelterInstancePage;
