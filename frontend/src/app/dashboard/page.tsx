'use client'
import React, { useState } from 'react';
import UploadComponent from './_components/Upload/UploadComponent';
import { CopyBlock, dracula } from "react-code-blocks";
import { useAuthToken } from '../_utils/auth_utils';
import { putAuthorized } from '../_utils/api_utils';

function App({ isAuthenticated, setIsAuthenticated }: any) {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [conversionData, setConversionData] = useState<any>(null);
  const [activeView, setActiveView] = useState('upload');
  const { withTokenRotation } = useAuthToken({ isAuthenticated, setIsAuthenticated });

  const handleFileUpload = async (file: File) => {
    const file_name = file.name;
    try {
      const response = await withTokenRotation(() => {
        const formData = new FormData();
        formData.append('invoice_file', file);
        return putAuthorized(`upload/${encodeURIComponent(file_name)}`, formData, 'multipart/form-data');
      })();

      console.log('Upload response:', response);
      setUploadedFile(file);
      setConversionData(JSON.parse(response.json));
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
              <h1 style={{ marginBottom: '3rem' }}>Upload Invoice</h1>
              <UploadComponent uploadedFile={uploadedFile} onFileUpload={handleFileUpload} />
            </div>
            {conversionData && (
              <CopyBlock
                text={JSON.stringify(conversionData, null, 2)}
                language="json"
                showLineNumbers={true}
                theme={dracula}
                codeBlock
                customStyle={{
                  width: '40%',
                  height: '70%',
                  marginRight: '1rem',
                  marginTop: '6rem',
                }}
              />
            )}
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
