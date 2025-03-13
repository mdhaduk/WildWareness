import { useState, useEffect} from 'react';
import { useParams, useNavigate, Link} from 'react-router-dom';
import axios from 'axios';
import Map from '../components/Map';

const NewsReportInstancePage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [report, setReport] = useState(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await axios.get(`https://api.wildwareness.net/news/${id}`);
        const modifiedResponse = {
            ...response.data, // Spread all properties from response.data
        };
        if(modifiedResponse.text_summary === "No summary, use description") {
            modifiedResponse.text_summary = modifiedResponse.description
        }
        
        setReport(modifiedResponse);
      } catch (error) {
        console.error("Error fetching report details:", error);
      }
    };
    fetchReport();
  }, [id]);

  if (!report) {
    return <div>Loading...</div>;
  }

  const nearbyWildfires = [];
  for (let i = 0; i < report.wildfires.length; i++) {
    nearbyWildfires.push(
      <li key={i}>
            <Link to={`/wildfire_incidents/${report.wildfires[i].id}`}>
              {report.wildfires[i].name}
            </Link>
      </li>
    );
  }

  const nearbyShelters = [];
  for (let i = 0; i < report.shelters.length; i++) {
    nearbyShelters.push(
      <li key={i}>
            <Link to={`/shelters/${report.shelters[i].id}`}>
              {report.shelters[i].name}
            </Link>
      </li>
    );
  }

  return (
    <div className="container mt-5">
      <h3><strong>{report.title}</strong></h3>
      {report.source && <p>Source: {report.source}</p>}
      {report.url && <a href={report.url} target="_blank" rel="noopener noreferrer">Read Full Article</a>}

      <div className="row my-4 justify-content-center">
        <div className="col-md-8 text-center mb-4">
          <img
            src={report.image_url || '/default-placeholder.jpg'}
            alt={report.title}
            className="img-fluid"
            style={{ height: '300px', width: '600px', objectFit: 'cover' }}
            onError={(e) => { e.target.src = '/default-placeholder.jpg'; }}
          />
        </div>
      </div>

      <div className="container-fluid my-4">
        <h5><strong>Description:</strong></h5>
        <p>{report.text_summary || "No description available."}</p>
      </div>

      <Map address={report.locations[0]} fireName={report.title} />

      <div className="container-fluid my-4">
        <h5><strong>Attributes:</strong></h5>
        <ul className="list-group list-group-flush">
          <li className="list-group-item text-wrap"><strong>Title:</strong> {report.title}</li>
          <li className="list-group-item text-wrap"><strong>Source:</strong> {report.source}</li>
          <li className="list-group-item text-wrap"><strong>Date:</strong> {report.published_at}</li>
          <li className="list-group-item text-wrap"><strong>Author:</strong> {report.author}</li>
          <li className="list-group-item text-wrap"><strong>Categories:</strong> {report.categories}</li>
          <li className="list-group-item text-wrap"><strong>Estimated Reading Time (Minutes):</strong> {report.reading_time}</li>
        </ul>
      </div>
      <br />
      <div className="row">
        <h5 className=''><strong>Nearby Wildfires:</strong></h5>
                {report.wildfires.length > 0 ? (
                    report.wildfires.map((wildfire) => (
                        <div key={wildfire.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={wildfire.url} alt={wildfire.name}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {wildfire.name}</li>
                                    <li className="list-group-item"><strong>County:</strong> {wildfire.county}</li>
                                    <li className="list-group-item"><strong>Location:</strong> {wildfire.location}</li>
                                    <li className="list-group-item"><strong>Year:</strong> {wildfire.year}</li>
                                    <li className="list-group-item"><strong>Acres Burned:</strong> {wildfire.acres_burned}</li>
                                </ul>
                                <div className="card-body text-center">
                                    <Link to={`/incidents/${wildfire.id}`} className="btn btn-primary">Read More</Link>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-center">Loading...</p>
                )}
        </div>
        <br />
        <div className="row">
        <h5 className=''><strong>Nearby Shelters:</strong></h5>
                {report.shelters.length > 0 ? (
                    report.shelters.map((shelter) => (
                        <div key={shelter.id} className="col-md-4 mb-4">
                            <div className="card" style={{ width: '22rem' }}>
                                <img className="card-img" src={shelter.imageUrl} alt={shelter.name}/>
                                <ul className="list-group list-group-flush">
                                    <li className="list-group-item"><strong>Name:</strong> {shelter.name}</li>
                                    <li className="list-group-item"><strong>Address:</strong> {shelter.address}</li>
                                    <li className="list-group-item"><strong>Phone:</strong> {shelter.phone}</li>
                                    <li className="list-group-item"><strong>Website:</strong> {shelter.website}</li>
                                    <li className="list-group-item"><strong>Rating:</strong> {shelter.rating}</li>
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

      <div>
        <button className="btn btn-secondary mb-3" onClick={() => navigate('/news')}>Go Back</button>
      </div>
    </div>
  );
};

export default NewsReportInstancePage;
