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
import Settings from './components/Settings';
import ThemeContext from './ThemeContext';
import './App.css'; // Import the CSS file
import { supabase } from './supabaseClient'

function App() {
  const [theme, setTheme] = useState('dark');
  const [session, setSession] = useState(null);

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
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/api" element={<Api />} />
          <Route path="/docs" element={<Docs />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/settings" element={<Settings session={session} />} />
        </Routes>
      </Router>
    </ThemeContext.Provider>
  );
}

export default App;