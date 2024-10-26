import './Mapping.css';
import PlacesAutocomplete, { geocodeByAddress, getLatLng } from 'react-places-autocomplete';
import React, { useState } from 'react';
import { GoogleMap, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '85vh',
};

function SearchAddress({ setCoordinates, setAddressParent, setRecent }) {
  const center = {
    lat: 33.7490,
    lng: -84.3880,
  };

  const onMapClick = (event) => {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    const newCoordinates = { lat, lng };

    setCoordinates(newCoordinates);
    setRecent(true);
    setCoordinatesState(newCoordinates);
  }

  const [address, setAddress] = useState("");
  const [coordinates, setCoordinatesState] = useState({
    lat: null,
    lng: null
  });

  const handleSelect = async (value) => {
    try {
      const results = await geocodeByAddress(value);
      const ll = await getLatLng(results[0]);
      
      setRecent(false);
      setAddress(value);
      setAddressParent(value);

      setCoordinatesState(ll);
      setCoordinates(ll);
    } catch (error) {
      console.error("Error fetching address:", error);
      alert("Could not find the address. Please try again.");
    }
  };

  return (
    <div className="SearchAddress">
      <div className="search-container">
        <PlacesAutocomplete
          value={address}
          onChange={setAddress}
          onSelect={handleSelect}
        >
          {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
            <div>
              <input
                {...getInputProps({
                  placeholder: 'Search Places ...',
                  className: 'location-search-input',
                })}
              />
              <div className={`autocomplete-dropdown-container ${suggestions.length > 0 ? 'visible' : ''}`}>
                {loading && <div>Loading...</div>}
                {suggestions.map(suggestion => {
                  const className = suggestion.active
                    ? 'suggestion-item--active'
                    : 'suggestion-item';
                  return (
                    <div
                      {...getSuggestionItemProps(suggestion, {
                        className,
                      })}
                      key={suggestion.placeId} // Add a unique key
                    >
                      <span>{suggestion.description}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </PlacesAutocomplete>
      </div>

      <GoogleMap
        onClick={onMapClick}
        mapContainerStyle={mapContainerStyle}
        center={coordinates.lat !== null ? coordinates : center}
        zoom={8}
      >
        {coordinates.lat !== null && (
          <Marker position={coordinates} title="You selected this location" />
        )}
      </GoogleMap>
    </div>
  );
}

export default SearchAddress;