// frontend/src/components/Upload/UploadComponent.js
import React, { useRef, useState } from 'react';

function UploadComponent({ onFileUpload, uploadedFile }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  const handleAnalyze = () => {
    // TODO: Backend analysis logic
    // Implement API call to process uploaded file
  };

  const handleDownload = () => {
    // TODO: Backend download logic for different formats
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
      backgroundColor: '#f0f2f5',
      borderRadius: '10px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    }}>
      <div 
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
        style={{
          width: '400px',
          height: '200px',
          border: `2px dashed ${dragActive ? '#1877f2' : '#ccc'}`,
          borderRadius: '10px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s',
          backgroundColor: dragActive ? 'rgba(24, 119, 242, 0.1)' : 'white'
        }}
      >
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".pdf,.png,.jpg,.jpeg"
          style={{ display: 'none' }}
        />
        {uploadedFile ? (
          <p>{uploadedFile.name}</p>
        ) : (
          <>
            <p>Drag & Drop or Click to Upload</p>
            <p>Supported: PDF, PNG, JPG</p>
          </>
        )}
      </div>
      
      <div style={{
        marginTop: '20px',
        display: 'flex',
        gap: '15px'
      }}>
        <button 
          onClick={handleAnalyze}
          style={{
            padding: '10px 20px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
          disabled={!uploadedFile}
        >
          Analyze
        </button>
        <button 
          onClick={handleDownload}
          style={{
            padding: '10px 20px',
            backgroundColor: '#1877f2',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
          disabled={!uploadedFile}
        >
          Download Options
        </button>
      </div>
    </div>
  );
}

export default UploadComponent;