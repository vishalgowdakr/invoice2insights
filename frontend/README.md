# Invoice Converter Application

## Overview
This is a full-stack web application that allows users to convert invoices from PDF and image formats to CSV, JSON, and PNG formats with advanced visualization capabilities.

## Features
- User Authentication (Signup/Login)
- File Upload (PDF, PNG, JPG)
- Invoice Data Extraction
- Multiple Format Conversion (CSV, JSON, PNG)
- Interactive Data Visualization
- Download Options

## Technologies Used
### Frontend
- React.js
- Recharts (Visualization)
- CSS (Custom Styling)

### Backend
- Spring Boot
- Apache PDFBox (PDF Processing)
- Tesseract OCR (Image Text Extraction)
- OpenCSV (CSV Conversion)

## Prerequisites
- Node.js (v14+)
- npm (v6+)
- Java JDK 11+
- Maven

## Installation Steps

### Frontend Setup
```bash
# Clone the repository
git clone <repository-url>

# Navigate to frontend directory
cd invoice-converter-frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Backend Setup
```bash
# Navigate to backend directory
cd invoice-converter-backend

# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

## Environment Configuration
- Create `.env` files for frontend and backend
- Configure database connections
- Set up security tokens

## Running Tests
```bash
# Frontend Tests
npm test

# Backend Tests
mvn test
```

## Deployment
- Dockerization scripts
- CI/CD pipeline configurations

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License