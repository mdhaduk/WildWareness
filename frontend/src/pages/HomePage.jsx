import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';  // Make sure you import Link from react-router-dom

function HomePage() {
    return (
        <div className="container">
            <div className="row w-100">
                <div className="col-lg-6 d-flex flex-column align-items-center justify-content-center text-center px-5">
                    <h1>About <span className="fire-text">WildWareness</span></h1>
                    <p>WildWareness is a web application designed to provide real-time wildfire information, emergency shelter locations, and community-reported fire updates in the state of California.</p>
                    <p><strong>Platform serves:</strong> People in wildfire-affected areas needing information on active fires and emergency shelters, as well as volunteers and first responders looking to help communities.</p>
                    <p><strong>Users can</strong></p>
                    <ul className="text-start">
                        <li>Track active wildfires with real-time data.</li>
                        <li>Find emergency shelters near affected areas.</li>
                        <li>View and submit community reports on wildfire conditions.</li>
                    </ul>
                </div>

                <div className="col-lg-6 d-flex align-items-center justify-content-center mb-5">
                <div id="carouselExampleAutoplaying" className="carousel slide" data-bs-ride="carousel" style={{ maxWidth: '900px', maxHeight: '500px' }} data-testid="carousel">
                        <div className="carousel-inner">
                            <div className="carousel-item active">
                                <img src="https://npr.brightspotcdn.com/dims3/default/strip/false/crop/4964x3309+0+0/resize/1300/quality/85/format/webp/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F12%2F42%2Fcdcddc04453da38799e99c976828%2Fgettyimages-2193654527.jpg" className="d-block w-100" alt="Wildfire"/>
                            </div>
                            <div className="carousel-item">
                                <img src="https://npr.brightspotcdn.com/dims3/default/strip/false/crop/3000x2000+0+0/resize/1300/quality/85/format/webp/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2F55%2Fc1%2Fc17a446247188b3dc17815e689ee%2Fla-fires-key-moments-01.jpg" className="d-block w-100" alt="Emergency Shelter"/>
                            </div>
                            <div className="carousel-item">
                                <img src="https://npr.brightspotcdn.com/dims3/default/strip/false/crop/3000x2000+0+0/resize/1300/quality/85/format/webp/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Faf%2F52%2Fc9c0f3bd4a18a25ca377aff4cdbf%2Fla-fires-key-moments-02.jpg" className="d-block w-100" alt="Firefighters"/>
                            </div>
                        </div>
                        <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
                            <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span className="visually-hidden">Previous</span>
                        </button>
                        <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
                            <span className="carousel-control-next-icon" aria-hidden="true"></span>
                            <span className="visually-hidden">Next</span>
                        </button>
                    </div>
                </div>

                <div className="row row-cols-1 row-cols-md-3 d-flex justify-content-center g-4">
                    <div className="card" style={{ width: '22rem', height: "26rem"}}>
                        {/* Image */}
                        <img className="card-img-top mx-auto d-block" style={{width: "230px", height: "230px"}}src="data:image/png;base64,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"
                        />
                        
                        <div className="card-body">
                            {/* Title with large font */}
                            <h5 className="card-title text-center" style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'maroon', wordWrap: 'break-word' }}>
                                Wildfire Incidents
                            </h5>
                            
                            {/* Short Description */}
                            <p className="card-text text-center" style={{ fontSize: '1rem', color: '#6c757d', whiteSpace: 'normal' }}>
                                Learn more about wildfires in your area
                            </p>
                            
                            {/* Read More Button */}
                            <div className="text-center">
                                <Link to={`/incidents`} className="btn btn-primary">Read More</Link>
                            </div>
                        </div>
                    </div>
                    <div className="card" style={{ width: '22rem', height: '26rem'}}>
                        {/* Image */}
                        <img className="card-img-top mx-auto" style={{width: "220px", height: "220px"}} src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-l6wNUpAcbN_I-awMgWQEt5k02D9pYFDJ1Q&s" />
                        
                        <div className="card-body">
                            {/* Title with large font */}
                            <h5 className="card-title text-center" style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'maroon', wordWrap: 'break-word' }}>
                                Shelters
                            </h5>
                            
                            {/* Short Description */}
                            <p className="card-text text-center" style={{ fontSize: '1rem', color: '#6c757d', whiteSpace: 'normal' }}>
                                Find shelters near you
                            </p>
                            
                            {/* Read More Button */}
                            <div className="text-center">
                                <Link to={`/shelters`} className="btn btn-primary">Read More</Link>
                            </div>
                        </div>
                    </div>
                    <div className="card" style={{ width: '22rem', height: '26rem'}}>
                        {/* Image */}
                        <img className="card-img-top" src="data:image/jpeg;base64,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" />
                        
                        <div className="card-body">
                            {/* Title with large font */}
                            <h5 className="card-title text-center" style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'maroon', wordWrap: 'break-word' }}>
                                News Reports
                            </h5>
                            
                            {/* Short Description */}
                            <p className="card-text text-center" style={{ fontSize: '1rem', color: '#6c757d', whiteSpace: 'normal' }}>
                                Read relevant news articles and reports
                            </p>
                            
                            {/* Read More Button */}
                            <div className="text-center">
                                <Link to={`/news`} className="btn btn-primary">Read More</Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Adding the Card */}
           
            
      
        </div>
    );
}

export default HomePage;
