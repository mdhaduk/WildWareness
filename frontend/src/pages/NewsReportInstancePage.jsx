import { useState, useEffect} from 'react';
import { useParams, useNavigate, Link} from 'react-router-dom';
import axios from 'axios';
import Map from '../components/Map';
import WildfireCard from '../components/WildfireCard';
import ShelterCard from '../components/ShelterCard';

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
            src={report.image_url}
            alt={report.title}
            className="img-fluid"
            style={{ height: '300px', width: '600px', objectFit: 'cover' }}
            onError={(e) => { e.target.src = 'https://s.hdnux.com/photos/0/0/0/10802857/0/900x0.jpg'; }}
          />
        </div>
      </div>

      <div className="container-fluid my-4">
        <h5><strong>Description:</strong></h5>
        <p>{report.text_summary === "No summary, use description" ? report.description : report.text_summary}</p>
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
        <h5 className=''><strong>Nearby Shelters:</strong></h5>
                {report.shelters.length > 0 ? (
                    report.shelters.map((shelter) => (
                      <ShelterCard
                      key={shelter.id}
                      shelter={shelter}
     
                    />
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
