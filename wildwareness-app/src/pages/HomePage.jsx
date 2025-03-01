import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function HomePage() {
    return (
        <div className="container-fluid hero-section">
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

                <div className="col-lg-6 d-flex align-items-center justify-content-center">
                    <div id="carouselExampleAutoplaying" className="carousel slide" data-bs-ride="carousel" style={{ maxWidth: '900px', maxHeight: '500px' }}>
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
            </div>
        </div>
    );
}

export default HomePage;
