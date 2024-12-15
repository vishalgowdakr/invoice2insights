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
  };


  return (
    <div className="upload-container">
      <div className="background-shapes">
        <div
          className={`upload-area ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept=".pdf,.png,.jpg,.jpeg"
            style={{ display: 'none' }}
          />
          <div className="upload-content">
            <div className="file-icon">📄</div>
            {uploadedFile ? (
              <>
                <div className="upload-text">{uploadedFile.name}</div>
                <div className="upload-subtext">File ready for processing</div>
              </>
            ) : (
              <>
                <div className="upload-text">Drag & Drop or Click to Upload</div>
                <div className="upload-subtext">Supported: PDF, PNG, JPG</div>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="button-container">
        <button
          onClick={handleAnalyze}
          className="action-button analyze-button"
          disabled={!uploadedFile}
        >
          Analyze
        </button>
      </div>

      <style>
        {`
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }

          body {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            font-family: 'Arial', sans-serif;
          }

          .upload-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
            position: relative;
            max-width: 800px;
            margin: 0 auto;
            min-height: 500px;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            animation: containerFadeIn 0.8s ease-out;
          }

          .background-shapes {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
            z-index: -1;
          }

          .background-shapes::before,
          .background-shapes::after {
            content: '';
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            animation: shapeMove 20s infinite alternate ease-in-out;
            opacity: 0.1;
          }

          .background-shapes::before {
            top: -200px;
            right: -100px;
            animation-delay: -5s;
          }

          .background-shapes::after {
            bottom: -200px;
            left: -100px;
            background: linear-gradient(45deg, #764ba2, #667eea);
          }

          .upload-area {
            position: relative;
            width: 100%;
            height: 300px;
            border: 3px dashed #cbd5e0;
            border-radius: 20px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
          }

          .upload-area::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            opacity: 0;
            transition: opacity 0.3s ease;
          }

          .upload-area.active {
            border-color: #667eea;
            transform: scale(1.02);
          }

          .upload-area.active::before {
            opacity: 1;
          }

          .button-container {
            display: flex;
            gap: 30px;
            margin-top: 400px;
            justify-content: center;
            width: 100%;
          }

          .action-button {
            padding: 15px 30px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
          }

          .action-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
            transform: translateX(-100%);
            transition: transform 0.5s ease;
          }

          .action-button:hover::before {
            transform: translateX(100%);
          }

          .analyze-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
          }

          .action-button:disabled {
            background: #cbd5e0;
            cursor: not-allowed;
            box-shadow: none;
          }

          @keyframes shapeMove {
            0% {
              transform: translate(0, 0) rotate(0deg) scale(1);
            }
            100% {
              transform: translate(50px, 50px) rotate(180deg) scale(1.2);
            }
          }

          @keyframes containerFadeIn {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          @keyframes floatingAnimation {
            0% {
              transform: translateY(0);
            }
            50% {
              transform: translateY(-10px);
            }
            100% {
              transform: translateY(0);
            }
          }

          .upload-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            z-index: 1;
            position: relative;
            animation: floatingAnimation 3s ease-in-out infinite;
          }

          .file-icon {
            width: 64px;
            height: 64px;
            margin-bottom: 20px;
            border-radius: 12px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
          }

          .upload-text {
            font-size: 18px;
            color: #2d3748;
            margin-bottom: 10px;
            font-weight: 600;
          }

          .upload-subtext {
            font-size: 14px;
            color: #718096;
          }

          @media (max-width: 768px) {
            .upload-container {
              padding: 30px;
            }

            .button-container {
              flex-direction: column;
              gap: 20px;
              margin-top: 300px;
            }

            .action-button {
              width: 100%;
              padding: 12px 20px;
              font-size: 14px;
            }
          }
        `}
      </style>
    </div>
  );
}

export default UploadComponent;
