// frontend/src/App.js
import React, { useState } from 'react';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import UploadComponent from './components/Upload/UploadComponent';
import GraphComponent from './components/Visualization/GraphComponent';
import './styles/main.css';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // State to manage login status
  const [activeView, setActiveView] = useState('login'); // State for the active view
  const [uploadedFile, setUploadedFile] = useState(null); // State for the uploaded file
  const [conversionData, setConversionData] = useState(null); // State for conversion data

  const handleLogin = () => {
    // Simulate login logic
    setIsLoggedIn(true);
    setActiveView('upload');
  };

  const handleSignup = () => {
    // Simulate signup logic
    setIsLoggedIn(true);
    setActiveView('upload');
  };

  const handleFileUpload = async (file) => {
    // Simulate file upload logic
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Placeholder for backend API call
      setUploadedFile(file);
      setConversionData({
        // Placeholder for converted data
        csvData: [['Header1', 'Header2'], ['Row1', 'Row2']],
        jsonData: { key1: 'value1', key2: 'value2' },
        graphData: [{ x: 1, y: 2 }, { x: 2, y: 3 }]
      });
    } catch (error) {
      console.error('Upload failed', error);
    }
  };

  const handleLogout = () => {
    // Reset login state and view
    setIsLoggedIn(false);
    setActiveView('login');
    setUploadedFile(null);
    setConversionData(null);
  };

  const renderView = () => {
    if (!isLoggedIn) {
      // Show login/signup screens if not logged in
      return activeView === 'login' ? (
        <Login onLogin={handleLogin} onSwitchToSignup={() => setActiveView('signup')} />
      ) : (
        <Signup onSignup={handleSignup} onSwitchToLogin={() => setActiveView('login')} />
      );
    }

    // Show upload and visualization if logged in
    return (
      <div className="app-container">
        <UploadComponent onFileUpload={handleFileUpload} uploadedFile={uploadedFile} />
        {conversionData && (
          <GraphComponent
            data={conversionData}
            onDownload={() => {
              console.log('Download logic to be implemented');
            }}
          />
        )}
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    );
  };

  return <div className="main-app">{renderView()}</div>;
}

export default App;
