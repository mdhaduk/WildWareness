import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
const API_KEY = "AIzaSyDJPeWEbVWBXRGI_W3FIzqkffL41rQVuOA";

const mapContainerStyle = { height: "500px", width: "50%" };

const Map = ({ address, fireName }) => {
  const [coordinates, setCoordinates] = useState(null);

  useEffect(() => {
    const fetchCoordinates = async () => {
      try {
        const response = await fetch(
          `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${API_KEY}`
        );
        const data = await response.json();
        if (data.results.length > 0) {
          setCoordinates({
            lat: data.results[0].geometry.location.lat,
            lon: data.results[0].geometry.location.lng,
          });
        }
      } catch (error) {
        console.error("Error fetching coordinates:", error);
      }
    };

    if (address) {
      fetchCoordinates();
    }
  }, [address]);

  return coordinates ? (
    <MapContainer center={[coordinates.lat, coordinates.lon]} zoom={10} style={mapContainerStyle}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
      {/* Marker for wildfire */}
      <Marker position={[coordinates.lat, coordinates.lon]}>
        <Popup>
          <strong>{fireName}</strong>
          <br />
          Location: {address}
        </Popup>
      </Marker>
    </MapContainer>
  ) : (
    <p>Loading map...</p>
  );
};

export default Map;
