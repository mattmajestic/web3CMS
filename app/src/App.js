// App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavBar from './components/NavBar';
import Home from './components/Home';
import Auth from './components/Auth';
import Api from './components/Api';
import Docs from './components/Docs';
import Chat from './components/Chat';
import Terms from './components/Terms';
import Deploy from './components/Deploy';
import Workspace from './components/Workspace';
import Database from './components/Database';
import Pricing from './components/Pricing';
import Settings from './components/Settings';
import Request from './components/Request';
import Cloud from './components/Cloud';
import ThemeContext from './ThemeContext';
import './App.css'; // Import the CSS file
import { supabase } from './supabaseClient'
import { isMobile } from 'react-device-detect';
import Modal from 'react-modal';

function App() {
  const [theme, setTheme] = useState('dark');
  const [session, setSession] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(isMobile);

  const closeModal = () => {
    setModalIsOpen(false);
  };

  useEffect(() => {
    setSession(supabase.auth.session);

    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });
  }, []);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
  };

  useEffect(() => {
    document.body.className = '';
    document.body.classList.add(theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <Router>
        <NavBar session={session} />
        <Modal
          isOpen={modalIsOpen}
          onRequestClose={closeModal}
          style={{
            overlay: { backgroundColor: 'rgba(0, 0, 0, 0.5)' },
            content: {
              color: 'white',
              backgroundColor: '#17072B',
              padding: '20px',
              borderRadius: '10px',
              width: '50%',
              height: '50%',
              position: 'absolute',
              top: '25%',
              left: '25%'
            }
          }}
          contentLabel="Mobile Warning"
        >
          <h2>Mobile Optimization Coming Soon.</h2>
          <button 
            onClick={closeModal} 
            style={{ 
              backgroundColor: 'white', 
              color: '#17072B', 
              padding: '10px', 
              borderRadius: '5px', 
              border: 'none', 
              cursor: 'pointer' 
            }}
          >
            Proceed
          </button>
        </Modal>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/api" element={<Api />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/chat" element={<Chat session={session} />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/workspace" element={<Workspace session={session} />} />
          <Route path="/deploy" element={<Deploy session={session} />} />
          <Route path="/database" element={<Database session={session} />} />
          <Route path="/settings" element={<Settings session={session} />} />
          <Route path="/cloud" element={<Cloud session={session} />} />
          <Route path="/request" element={<Request session={session} />} />
        </Routes>
      </Router>
    </ThemeContext.Provider>
  );
}

export default App;