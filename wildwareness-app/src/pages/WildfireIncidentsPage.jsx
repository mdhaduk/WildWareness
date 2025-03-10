import { useState, useEffect} from 'react';
import { useParams, useNavigate} from 'react-router-dom';
import axios from 'axios';
import Map from '../components/Map';

const WildfireIncidentsPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [wildfire, setWildFire] = useState(null);

  useEffect(() => {
    const fetchWildFire = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/wildfire_incidents/${id}`);
        setWildFire(response.data);
      } catch (error) {
        console.error("Error fetching wildfire details:", error);
      }
    };
    fetchWildFire();
  }, [id]);

  if (!wildfire) {
    return <div>Loading...</div>;
  }


  return (
    <div className="container mt-5">
      <h3><strong>{wildfire.name}</strong></h3>
      <p>{wildfire.location}</p>

      <div className="row my-4 justify-content-center">
        <div className="col-md-8 text-center mb-4">
          <img
            src={wildfire.url || '/default-placeholder.jpg'}
            alt={wildfire.name}
            className="img-fluid"
            style={{ height: '300px', width: '600px', objectFit: 'cover' }}
            onError={(e) => { e.target.src = '/default-placeholder.jpg'; }}
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
        </ul>
      </div>

      <div>
        <button className="btn btn-secondary mb-3" onClick={() => navigate('/incidents')}>Go Back</button>
      </div>
    </div>
  );
};

export default WildfireIncidentsPage;
