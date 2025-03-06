import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const mapContainerStyle = { height: "500px", width: "50%" };

const WildfireMap = ({ latitude, longitude, fireName }) => {
  return (
    <MapContainer center={[latitude, longitude]} zoom={10} style={mapContainerStyle}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
      {/* Marker for wildfire */}
      <Marker position={[latitude, longitude]}>
        <Popup>
          <strong>{fireName}</strong>
          <br />
          Location: {latitude}, {longitude}
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default WildfireMap;
