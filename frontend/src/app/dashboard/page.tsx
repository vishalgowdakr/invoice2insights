'use client'
import React, { useEffect, useState } from 'react';
import UploadComponent from './_components/Upload/UploadComponent';
import { CopyBlock, dracula } from "react-code-blocks";
import { useAuthToken } from '../_utils/auth_utils';
import { postAuthorized } from '../_utils/api_utils';
import AnalyzeComponent from './_components/Analyze/Analyze';

export type CallAnalyzeStatus = 'not_called' | 'in_progress' | 'completed'

function App({ isAuthenticated, setIsAuthenticated }: any) {
  // State for multiple uploaded files
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [activeView, setActiveView] = useState('upload');
  // State for file type selection (common for the batch)
  const [fileType, setFileType] = useState<string>('pdf');
  const { withTokenRotation } = useAuthToken({ isAuthenticated, setIsAuthenticated });
  const [callAnalyze, setCallAnalyze] = useState<CallAnalyzeStatus>('not_called');
  const [uploadId, setUploadId] = useState<number>(0);

  //useEffects
  useEffect(() => {
    if (callAnalyze === 'in_progress') {
      postAuthorized(`analyze/${uploadId}/`, {}, 'application/json').then(() => {
        updateCallAnalyze('completed')
      });
    }
  }, [callAnalyze])

  const updateCallAnalyze = (status: CallAnalyzeStatus) => {
    setCallAnalyze(status);
  }

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
      setUploadId(response.id)
    } catch (error) {
      console.error('Upload failed', error);
    }
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
              <h1 style={{ marginBottom: '1rem' }}>Upload Invoice</h1>
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
                  <option value="png">PNG</option>
                  <option value="pdf">PDF</option>
                </select>
              </div>
              {/* Pass the updated props to support multiple files */}
              <UploadComponent uploadedFiles={uploadedFiles} onFileUpload={handleFileUpload} onAnalyze={setCallAnalyze} />
              {
                callAnalyze !== 'not_called' && (
                  <AnalyzeComponent />
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
          }}>
            <h1>Accounts Dashboard</h1>
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
                transition: 'background-color 0.2s ease-in-out'
              }}
              onMouseOver={(e) => (e.target as HTMLElement).style.backgroundColor = '#1d4ed8'}
              onMouseOut={(e) => (e.target as HTMLElement).style.backgroundColor = '#2563eb'}
            >
              Upload Invoice
            </button>
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
