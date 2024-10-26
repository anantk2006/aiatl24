import './App.css';
import SearchAddress from './mapping/Mapping';
import Proceed from './analysis/Proceed';
import Analysis from './analysis/Analysis';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import React, { useState } from 'react';

function App() {
  const [coordinates, setCoordinates] = useState({ lat: null, lng: null });
  const [address, setAddress] = useState("");

  const [coordRecent, setRecent] = useState(false); // coordinates: True -> coordinates  else Address

  return (
    <Router>
      <div className='Main'>
        <Routes>
          <Route path="/" element={
            <div>
              <div className='main-upper'>
                <SearchAddress setCoordinates={setCoordinates} setAddressParent={setAddress} setRecent={setRecent}/>
              </div>
              
              <div className='main-lower'>
                {!coordRecent ? (
                  <div className='data'>
                    <p>Selected Address: {address}</p>
                  </div>
                ) : (
                  <div className='data'>
                    <p className='data-txt'>Selected Latitude: {Math.round(coordinates.lat * 100) / 100}</p>
                    <p className='data-txt'>Selected Longitude: {Math.round(coordinates.lng * 100) / 100}</p>
                  </div>)
                
                }
                <Proceed className='button' coordinates={coordinates} /> {/* Pass coordinates here */}
              </div>
            </div>
          } />
          
          <Route path="/analysis" element={<Analysis coordinates={coordinates} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;