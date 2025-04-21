import { useState, useEffect} from 'react';
import { useParams, useNavigate, Link} from 'react-router-dom';
import axios from 'axios';
import Map from '../components/Map';
import ShelterCard from '../components/ShelterCard';
import ReportCard from '../components/ReportCard';

const WildfireIncidentsPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [wildfire, setWildFire] = useState(null);

  useEffect(() => {
    const fetchWildFire = async () => {
      try {
        const response = await axios.get(`https://api.wildwareness.net/wildfire_incidents/${id}`);
        console.log(response.data)
        setWildFire(response.data);
      } catch (error) {
        console.error("Error fetching wildfire details:", error);
      }
    };
    fetchWildFire();
  }, [id]);

  if (!wildfire) {
    return <div className='text-center'>Loading...</div>;
  }

  const nearbyShelters = [];
    for (let i = 0; i < wildfire.shelters.length; i++) {
      nearbyShelters.push(
        <li key={i}>
              <Link to={`/shelters/${wildfire.shelters[i].id}`}>
                {wildfire.shelters[i].name}
              </Link>
        </li>
      );
    }

    const nearbyNewsreports = [];
    for (let i = 0; i < wildfire.newsreports.length; i++) {
        nearbyNewsreports.push(
          <li key={i}>
                <Link to={`/news/${wildfire.newsreports[i].id}`}>
                  {wildfire.newsreports[i].name}
                </Link>
          </li>
        );
      }



  return (
    <div className="container mt-5">
      <h3><strong>{wildfire.name}</strong></h3>
      <p>{wildfire.location}</p>

      <div className="row my-4 justify-content-center">
        <div className="col-md-8 text-center mb-4">
          <img
            src={wildfire.url}
            alt={wildfire.name}
            className="img-fluid"
            style={{ height: '300px', width: '600px', objectFit: 'cover' }}
            onError={(e) => e.target.src = "https://i0.wp.com/calmatters.org/wp-content/uploads/2025/01/010725_Pacific-Palisades-Fire_GETTY_CM_WIDE_01.jpg?fit=2000%2C1125&ssl=1"}
          />
        </div>
      </div>

      <div className="container-fluid my-4">
        <h5><strong>Description:</strong></h5>
        <p>{wildfire.description || "No description available."}</p>
      </div>

      <Map address={wildfire.location} instanceName={wildfire.name} />

      <div className="container-fluid my-4">
        <h5><strong>Attributes:</strong></h5>
        <ul className="list-group list-group-flush">
          <li className="list-group-item text-wrap"><strong>Name:</strong> {wildfire.name}</li>
          <li className="list-group-item text-wrap"><strong>County:</strong> {wildfire.county}</li>
          <li className="list-group-item text-wrap"><strong>Location:</strong> {wildfire.location}</li>
          <li className="list-group-item text-wrap"><strong>Year:</strong> {wildfire.year}</li>
          <li className="list-group-item text-wrap"><strong>Acres Burned:</strong> {wildfire.acres_burned}</li>
          <li className="list-group-item text-wrap"><strong>Status:</strong> {wildfire.status}</li>
        </ul>
      </div>
      <div className="row">
        <h5 className=''><strong>Nearby Shelters:</strong></h5>
                {wildfire.shelters.length > 0 ? (
                    wildfire.shelters.map((shelter) => (
                      <ShelterCard
                        shelter={shelter}
                      />
                    ))
                ) : (
                    <p className="text-center">Loading...</p>
                )}
        </div>
        <br /> 
        <div className="row">
        <h5 className=''><strong>Nearby News Reports:</strong></h5>
                {wildfire.newsreports.length > 0 ? (
                    wildfire.newsreports.map((report) => ( 
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
        <button className="btn btn-secondary mb-3" onClick={() => navigate('/incidents')}>Go Back</button>
      </div>
    </div>
  );
};

export default WildfireIncidentsPage;
