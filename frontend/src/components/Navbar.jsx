import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg py-3" style={{ fontSize: '1.25rem' }}>
        <div className="container-fluid">
            <a className="navbar-brand fire-text" href="/" style={{ fontSize: '2rem', fontWeight: 'bold' }}>
            WildWareness
            </a>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto gap-3">
                <li className="nav-item"><a className="nav-link" href="/incidents">Wildfire Incidents</a></li>
                <li className="nav-item"><a className="nav-link" href="/shelters">Emergency Shelters</a></li>
                <li className="nav-item"><a className="nav-link" href="/news">Community Reports</a></li>
                <li className="nav-item"><a className="nav-link" href="/search">Search</a></li>
                <li className="nav-item"><a className="nav-link active" href="/about"><strong>About</strong></a></li>
            </ul>
            </div>
        </div>
    </nav>
  );
}

export default Navbar;
