import React, { useEffect, useState } from 'react';
import { GoogleMap, Circle } from '@react-google-maps/api';
import hurricaneData from './test.json'; // Adjust the path as necessary
import './Analysis.css'; // Import your CSS file

const Analysis = ({ coordinates }) => {
  const [hurricanes, setHurricanes] = useState({});

  useEffect(() => {
    setHurricanes(hurricaneData);
  }, []);

  const mapContainerStyle = {
    width: '30vw', // Width for the map
    height: '30vw', // Height for the map
  };

  const center = {
    lat: coordinates.lat || 27, // Example coordinates
    lng: coordinates.lng || -80,
  };

  return (
    <div className="analysis-container">
      <div className="outer-flex">
        <h2 className="map-header">Hurricane Paths in Your Area</h2>

        <div className="map-container">
          <GoogleMap
            mapContainerStyle={mapContainerStyle}
            center={center}
            zoom={8}
          >
            {Object.entries(hurricanes).map(([id, data]) =>
              data.points.map((point, index) => (
                <Circle
                  key={`${id}-${index}`}
                  center={{ lat: point.lat, lng: point.lng }}
                  radius={point.r * 50}
                  options={{
                    fillColor: data.color,
                    strokeColor: data.color,
                    fillOpacity: 1,
                    strokeWeight: 2,
                  }}
                />
              ))
            )}
          </GoogleMap>
        </div>
      </div>
      <div className="text-container">
        <h1>Breakdown</h1>
      </div>
    </div>
  );
};

export default Analysis;