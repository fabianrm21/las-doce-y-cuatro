import './App.css'
import badbunny from './assets/badbunny.jpg'
import dtmf from './assets/dtmf.png'
import { API_URL } from './settings/API_URL'

export default function App() {
  const handleSpotifyConnect = async () => {
    // Placeholder function - implement Spotify OAuth functionality here
    console.log('Spotify connect clicked')
    try{
      const response = await fetch(`${API_URL}/users/que se yo`, {
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include"
      });

      const data = await response.json();
      if (!response.ok){
        throw new Error(data.error);
      }

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
