import { BrowserRouter, Routes, Route } from "react-router-dom"
import './App.css'
import badbunny from './assets/badbunny.jpg'
import dtmf from './assets/dtmf.png'
import { API_URL } from './settings/API_URL'
import { v4 as uuidv4 } from "uuid"
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";


function getDeviceId() {
  let deviceId = localStorage.getItem("device_id");
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
    const savedDeviceId = localStorage.getItem("device_id");

    // If the user already has a device ID saved, reroute to the success page
    if (savedDeviceId) {
      console.log("attempting to reroute the user:", savedDeviceId);
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
  const [playbackTime, setPlaybackTime] = useState("");

  useEffect(() => {
    const getPlaybackTime = async () =>{
      try{
        // const deviceId = getDeviceId();
        const response = await fetch(`${API_URL}/playback-time/`, {
          method: "GET",
        });

        const data = await response.json();
        if (!response.ok){
          throw new Error(data.error);
        }
        setPlaybackTime(data.playback_time);
      } catch(error){
        alert(error);
      }
    }
    getPlaybackTime();
  }, []);

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

          <h1 className="main-title">Ya está</h1>
          <p className="subtitle">Ahora solo toca esperar <span className="emoji">🐰</span></p>
          <p className="subtitle">Y asegurarte de que tengas Spotify abierto y con cualquier canción en play antes de la hora 0</p>
          <PlaybackTimer playbackTime={playbackTime}/>
          
        </div>

        <footer className="footer">© 2025 Las Doce y Cuatro</footer>
      </div>
    </div>
  );
}

function PlaybackTimer({playbackTime}: {playbackTime: string}){
  const [timeRemaining, setTimeRemaining] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    total: 0
  });

  useEffect(() => {
    if (!playbackTime) return;

    const calculateTimeRemaining = () => {
      const now = new Date().getTime();
      const targetTime = new Date(playbackTime).getTime();
      const difference = targetTime - now;

      if (difference > 0) {
        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        setTimeRemaining({
          days,
          hours,
          minutes,
          seconds,
          total: difference
        });
      } else {
        setTimeRemaining({
          days: 0,
          hours: 0,
          minutes: 0,
          seconds: 0,
          total: 0
        });
      }
    };

    calculateTimeRemaining();
    const interval = setInterval(calculateTimeRemaining, 1000);

    return () => clearInterval(interval);
  }, [playbackTime]);

  if (!playbackTime) {
    return null;
  }

  if (timeRemaining.total <= 0) {
    return (
      <div className="timer-container">
        <p className="timer-message">¡Es hora! 🎵</p>
      </div>
    );
  }

  return (
    <div className="timer-container">
      <div className="timer-display">
        {timeRemaining.days > 0 && (
          <div className="time-unit">
            <span className="time-value">{timeRemaining.days}</span>
            <span className="time-label">{timeRemaining.days === 1 ? 'día' : 'días'}</span>
          </div>
        )}
        <div className="time-unit">
          <span className="time-value">{timeRemaining.hours}</span>
          <span className="time-label">{timeRemaining.hours === 1 ? 'hora' : 'horas'}</span>
        </div>
        <div className="time-unit">
          <span className="time-value">{timeRemaining.minutes}</span>
          <span className="time-label">{timeRemaining.minutes === 1 ? 'minuto' : 'minutos'}</span>
        </div>
        <div className="time-unit">
          <span className="time-value">{timeRemaining.seconds}</span>
          <span className="time-label">{timeRemaining.seconds === 1 ? 'segundo' : 'segundos'}</span>
        </div>
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