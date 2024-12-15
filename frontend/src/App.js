import React, { useState } from 'react';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import UploadComponent from './components/Upload/UploadComponent';
import GraphComponent from './components/Visualization/GraphComponent';
import './styles/main.css';
import { Link } from 'react-router-dom';  // Import Link component
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeView, setActiveView] = useState('login');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [conversionData, setConversionData] = useState(null);

  const handleLogin = () => {
    setIsLoggedIn(true);
    setActiveView('upload');
  };

  const handleSignup = () => {
    setIsLoggedIn(true);
    setActiveView('upload');
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploadedFile(file);
      setConversionData({
        csvData: [['Header1', 'Header2'], ['Row1', 'Row2']],
        jsonData: { key1: 'value1', key2: 'value2' },
        graphData: [{ x: 1, y: 2 }, { x: 2, y: 3 }]
      });
      console.log("Data set sucessfully")
    } catch (error) {
      console.error('Upload failed', error);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setActiveView('login');
    setUploadedFile(null);
    setConversionData(null);
  };

  const renderView = () => {
    if (!isLoggedIn) {
      return activeView === 'login' ? (
        <Login onLogin={handleLogin} onSwitchToSignup={() => setActiveView('signup')} />
      ) : (
        <Signup onSignup={handleSignup} onSwitchToLogin={() => setActiveView('login')} />
      );
    }

    return (
      <div style={{
        padding: '2rem',
        backgroundColor: 'transparent',
        minHeight: '100vh',
        transition: 'background-color 0.3s ease'
      }} className="app-container">
        <UploadComponent onFileUpload={handleFileUpload} uploadedFile={uploadedFile} />
        {conversionData && (
          <GraphComponent
          />
        )}
        <button 
          className="logout-button"
          onClick={handleLogout}
          style={{
            position: 'fixed',
            top: '1.5rem',
            right: '1.5rem',
            padding: '0.75rem 1.5rem',
            backgroundColor: '#ef4444',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            boxShadow: '0 2px 4px rgba(239, 68, 68, 0.1)',
            ':hover': {
              backgroundColor: '#dc2626',
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 6px rgba(239, 68, 68, 0.2)'
            },
            ':active': {
              transform: 'translateY(0)',
              boxShadow: '0 1px 2px rgba(239, 68, 68, 0.1)'
            }
          }}
        >
          Logout
        </button>
      </div>
    );
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)',  // Apply gradient directly to the background
      minHeight: '100vh',
      transition: 'all 0.3s ease'
    }} className="main-app">
      {renderView()}
    </div>
  );
}

export default App;
