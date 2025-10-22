import { BrowserRouter, Routes, Route } from "react-router-dom"
import './App.css'
import badbunny from './assets/badbunny.jpg'
import dtmf from './assets/dtmf.png'
import { API_URL } from './settings/API_URL'
import { v4 as uuidv4 } from "uuid"
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";


function getDeviceId() {
  let deviceId = localStorage.getItem("las_doce_y_cuatro_device_id");
  if (!deviceId){
    deviceId = uuidv4();
    localStorage.setItem("device_id", deviceId);
  }
  return deviceId;
}

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    // Get the device ID stored locally
    const savedDeviceId = localStorage.getItem("las_doce_y_cuatro_device_id");

    // If the user already has a device ID saved, reroute to the success page
    if (savedDeviceId) {
      navigate("/spotify-connected");
    }
  }, [navigate]);

  const handleSpotifyConnect = async () => {
    try{
      const deviceId = getDeviceId();
      const response = await fetch(`${API_URL}/users/link-account/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({device_id: deviceId}),
      });

      const data = await response.json();
      if (!response.ok){
        throw new Error(data.error);
      }

      window.location.href = data.auth_url;

    } catch(error){
      alert(error);
    }
  }

  return (
    <div className="app-container">
      {/* Background with gradient overlay */}
      <div className="background-section">
        <div className="background-image" style={{ backgroundImage: `url(${dtmf})` }}></div>
        <div className="gradient-overlay"></div>
        <div className="pattern-overlay"></div>
      </div>

      {/* Main content */}
      <div className="main-content">
        <div className="hero-section">
          {/* Hero image */}
          <div className="hero-image-container">
            <img
              src={badbunny}
              alt="Bad Bunny"
              className="hero-image"
            />
            <div className="image-glow"></div>
          </div>

          {/* Main heading */}
          <h1 className="main-title">
            Las Doce y Cuatro 
            {/* <span className="accent-text">x</span> Spotify */}
          </h1>

          {/* Subtitle */}
          <p className="subtitle">
            Conecta tu Spotify y únete a este evento
            <br />
            <span className="emoji">🐰</span>
          </p>

          {/* CTA Button */}
          <button 
            className="cta-button"
            onClick={handleSpotifyConnect}
          >
            <span className="button-text">Link Spotify Account</span>
            <div className="button-glow"></div>
          </button>

          {/* DTMF visual element */}
          <div className="dtmf-container">
            {/* <img src={dtmf} alt="DTMF" className="dtmf-image" /> */}
          </div>
        </div>

        {/* Footer */}
        <footer className="footer">
          © 2025 Las Doce y Cuatro
        </footer>
      </div>
    </div>
  )
}

function SpotifyConnected(){
  return (
    <div className="app-container">
      <div className="background-section">
        <div className="background-image" style={{ backgroundImage: `url(${dtmf})` }}></div>
        <div className="gradient-overlay"></div>
        <div className="pattern-overlay"></div>
      </div>

      <div className="main-content">
        <div className="hero-section">
          <div className="hero-image-container">
            <img src={badbunny} alt="Bad Bunny" className="hero-image" />
            <div className="image-glow"></div>
          </div>

          <h1 className="main-title">SUCCESS</h1>
          <p className="subtitle">Ahora solo toca esperar <span className="emoji">🐰</span></p>
          
        </div>

        <footer className="footer">© 2025 Las Doce y Cuatro</footer>
      </div>
    </div>
  );
}


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/spotify-connected" element={<SpotifyConnected />} />
      </Routes>
    </BrowserRouter>
  );
}
