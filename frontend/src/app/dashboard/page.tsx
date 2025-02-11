'use client'
import React, { useEffect, useState } from 'react';
import UploadComponent from './_components/Upload/UploadComponent';
import { useAuthToken } from '../_utils/auth_utils';
import { getAuthorized, postAuthorized } from '../_utils/api_utils';
import AnalyzeComponent from './_components/Analyze/Analyze';

export type CallAnalyzeStatus = 'not_called' | 'in_progress' | 'completed'

function App({ isAuthenticated, setIsAuthenticated }: any) {
  // State for multiple uploaded files
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [activeView, setActiveView] = useState('upload');
  // State for file type selection (common for the batch)
  const [fileType, setFileType] = useState<string>('png');
  const { withTokenRotation } = useAuthToken({ isAuthenticated, setIsAuthenticated });
  const [callAnalyze, setCallAnalyze] = useState<CallAnalyzeStatus>('not_called');
  const [uploadId, setUploadId] = useState<number>(0);

  // State for AnalyzeComponent
  const [analyzeProgress, setAnalyzeProgress] = useState<number>(0);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [hasUploaded, setHasUploaded] = useState<boolean>(false); // Track if files have been uploaded

  //useEffects
  useEffect(() => {
    let pollingInterval: any = null; // Changed type to 'any' to resolve Timeout type issue

    if (callAnalyze === 'in_progress') {
      setIsAnalyzing(true);
      pollingInterval = setInterval(() => {
        const fetchProgress = async () => {
          try {
            const response = await withTokenRotation(() =>
              getAuthorized(`analyze/${uploadId}/`) // Removed extra arguments to fix argument count issue
            )();
            console.log('Poll analyze progress response:', response);
            if (response && response.progress !== undefined) {
              setAnalyzeProgress(response.progress * 100); // Assuming progress is between 0 and 1
              if (response.status === 'Completed') {
                updateCallAnalyze('completed');
                setIsAnalyzing(false);
                setAnalyzeProgress(100);
                clearInterval(pollingInterval); // Correctly clear interval without non-null assertion
                pollingInterval = null;
              }
            }
          } catch (error) {
            console.error('Error polling analyze progress:', error);
            clearInterval(pollingInterval); // Correctly clear interval without non-null assertion
            pollingInterval = null;
            setIsAnalyzing(false); // Stop analyzing animation on error
          }
        };
        fetchProgress();
      }, 1000); // Poll every 1 second - adjust as needed
    } else if (callAnalyze === 'not_called') {
      setAnalyzeProgress(0);
      setIsAnalyzing(false);
      if (pollingInterval) {
        clearInterval(pollingInterval); // Clear interval if status changes to not_called
        pollingInterval = null;
      }
    }

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval); // Clear interval on component unmount
      }
    };
  }, [callAnalyze, uploadId, withTokenRotation]);

  const updateCallAnalyze = (status: CallAnalyzeStatus) => {
    setCallAnalyze(status);
  };

  // Modified to accept an array of Files
  const handleFileUpload = async (files: File[]) => {
    try {
      const response = await withTokenRotation(() => {
        const formData = new FormData();
        formData.append('file_type', fileType);
        files.forEach(file => {
          console.log('File:', file.name, file.type); // Add this
          formData.append('invoice_files', file);
        });
        return postAuthorized('upload/', formData, 'multipart/form-data');
      })();

      console.log('Upload response:', response);
      setUploadedFiles(files);
      setUploadId(response.id);
      setHasUploaded(true); // Set upload status to true after successful upload
      // updateCallAnalyze('in_progress'); // Do not start analyzing immediately after successful upload
    } catch (error) {
      console.error('Upload failed', error);
      updateCallAnalyze('not_called'); // Reset analyze status on upload failure
      setHasUploaded(false); // Ensure hasUploaded is false on failure
    }
  };

  const handleAnalyzeClick = () => {
    if (hasUploaded) {
      postAuthorized(`analyze/${uploadId}/`, {}, 'application/json');
      updateCallAnalyze('in_progress'); // Start analyzing on button click only if files are uploaded
    } else {
      alert("Please upload files first."); // Or any other user feedback
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  const renderView = () => (
    <div>
      {activeView === 'upload' ? (
        <div style={{
          padding: '2rem',
          backgroundColor: 'transparent',
          minHeight: '100vh',
          width: '100vw',
          transition: 'background-color 0.3s ease',
          marginLeft: 'auto',
          marginRight: 'auto'
        }} className="app-container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              onClick={() => setActiveView('dashboard')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 16px',
                fontSize: '14px',
                fontWeight: '500',
                color: 'white',
                backgroundColor: '#2563eb',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
                transition: 'background-color 0.2s ease-in-out'
              }}
              onMouseOver={(e) => (e.target as HTMLElement).style.backgroundColor = '#1d4ed8'}
              onMouseOut={(e) => (e.target as HTMLElement).style.backgroundColor = '#2563eb'}
            >
              <span>Open Dashboard</span>
            </button>
            <button
              onClick={handleLogout}
              hidden={!isAuthenticated}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '8px 16px',
                fontSize: '14px',
                fontWeight: '500',
                color: 'white',
                backgroundColor: '#dc2626',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
                transition: 'background-color 0.2s ease-in-out'
              }}
              onMouseOver={(e) => (e.target as HTMLElement).style.backgroundColor = '#b91c1c'}
              onMouseOut={(e) => (e.target as HTMLElement).style.backgroundColor = '#dc2626'}
            >
              <span>Logout</span>
            </button>
          </div>
          <div style={{
            display: 'flex',
            flex: '1',
            width: '100vw',
            justifyContent: 'space-around',
          }}>
            <div style={{
              textAlign: 'center',
              color: 'white',
              padding: '1rem',
              width: '50%',
            }}>
              <h1 style={{ marginBottom: '1rem', fontSize: '2rem', fontWeight: 'bolder' }}>Upload Invoice</h1>
              {/* File type selection for the batch */}
              <div style={{ marginBottom: '1rem' }}>
                <label htmlFor="fileTypeSelect" style={{ marginRight: '0.5rem' }}>
                  Select File Type:
                </label>
                <select
                  id="fileTypeSelect"
                  value={fileType}
                  onChange={(e) => setFileType(e.target.value)}
                  style={{ padding: '0.5rem', borderRadius: '4px', color: 'black' }}
                >
                  <option value="jpg">JPG</option>
                  <option value="pdf">PDF</option>
                  <option value="png">PNG</option>
                </select>
              </div>
              {/* Pass the updated props to support multiple files and handleAnalyzeClick */}
              <UploadComponent uploadedFiles={uploadedFiles} onFileUpload={handleFileUpload} onAnalyze={handleAnalyzeClick} />
              {hasUploaded && callAnalyze !== 'not_called' && (
                <AnalyzeComponent
                  progress={analyzeProgress}
                  isAnalyzing={isAnalyzing}
                  setActiveView={setActiveView}
                />
              )
              }
            </div>
          </div>
        </div>
      ) : (
        <div style={{
          width: '100vw',
          height: 'fit-content',
          background: 'linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}>
          <div style={{
            textAlign: 'start',
            color: 'white',
            padding: '1rem',
            display: 'flex',
            justifyContent: 'space-between',
            width: '80%',
            alignItems: 'center'
          }}>
            <h1 style={{
              fontSize: '2rem',
              fontWeight: 'bolder'
            }}>Accounts Dashboard</h1>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <button
                onClick={() => setActiveView('upload')}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 16px',
                  fontSize: '14px',
                  fontWeight: '500',
                  color: 'white',
                  backgroundColor: '#2563eb',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
                  transition: 'background-color 0.2s ease-in-out',
                  marginRight: '10px'
                }}
                onMouseOver={(e) => (e.target as HTMLElement).style.backgroundColor = '#1d4ed8'}
                onMouseOut={(e) => (e.target as HTMLElement).style.backgroundColor = '#2563eb'}
              >
                Upload Invoice
              </button>
              <button
                onClick={handleLogout}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '8px 16px',
                  fontSize: '14px',
                  fontWeight: '500',
                  color: 'white',
                  backgroundColor: '#dc2626',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
                  transition: 'background-color 0.2s ease-in-out'
                }}
                onMouseOver={(e) => (e.target as HTMLElement).style.backgroundColor = '#b91c1c'}
                onMouseOut={(e) => (e.target as HTMLElement).style.backgroundColor = '#dc2626'}
              >
                Logout
              </button>
            </div>
          </div>
          <iframe
            title="Dashboard"
            src="http://localhost:8088/login?token=1234abcd456&next=/superset/dashboard/1?standalone=3"
            width="80%"
            height="1200px"
            sandbox="allow-same-origin allow-scripts"
            style={{
              border: '0px'
            }}
          ></iframe>
        </div>
      )}
    </div>
  );

  return (
    <div style={{
      background: 'linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)',
      width: '100vw',
      minHeight: '100vh',
      transition: 'all 0.3s ease'
    }} className="main-app">
      {renderView()}
    </div>
  );
}

export default App;
