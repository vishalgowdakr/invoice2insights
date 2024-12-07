// frontend/src/components/Visualization/GraphComponent.js
import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';

function GraphComponent({ data, onDownload }) {
  const [graphType, setGraphType] = useState('bar');
  const [graphData, setGraphData] = useState([]);

  useEffect(() => {
    // TODO: Process data from backend conversion
    // Placeholder mock data
    const mockData = [
      { name: 'Jan', revenue: 4000, cost: 2400 },
      { name: 'Feb', revenue: 3000, cost: 1398 },
      { name: 'Mar', revenue: 2000, cost: 9800 },
      { name: 'Apr', revenue: 2780, cost: 3908 },
      { name: 'May', revenue: 1890, cost: 4800 },
      { name: 'Jun', revenue: 2390, cost: 3800 },
    ];
    setGraphData(mockData);
  }, [data]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const renderGraph = () => {
    switch(graphType) {
      case 'bar':
        return (
          <BarChart 
            width={600} 
            height={300} 
            data={graphData}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="revenue" fill="#8884d8" />
            <Bar dataKey="cost" fill="#82ca9d" />
          </BarChart>
        );
      case 'pie':
        return (
          <PieChart width={400} height={300}>
            <Pie
              data={graphData}
              cx={200}
              cy={150}
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="revenue"
            >
              {graphData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={COLORS[index % COLORS.length]} 
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        );
      default:
        return null;
    }
  };

  const handleDownload = (format) => {
    // TODO: Implement download logic for different formats
    // Backend API call to generate and download files
    console.log(`Downloading in ${format} format`);
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
      backgroundColor: '#f0f2f5'
    }}>
      <div style={{
        marginBottom: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <button 
          onClick={() => setGraphType('bar')}
          style={{
            padding: '10px',
            backgroundColor: graphType === 'bar' ? '#1877f2' : '#fff',
            color: graphType === 'bar' ? '#fff' : '#1877f2',
            border: '1px solid #1877f2',
            borderRadius: '5px'
          }}
        >
          Bar Graph
        </button>
        <button 
          onClick={() => setGraphType('pie')}
          style={{
            padding: '10px',
            backgroundColor: graphType === 'pie' ? '#1877f2' : '#fff',
            color: graphType === 'pie' ? '#fff' : '#1877f2',
            border: '1px solid #1877f2',
            borderRadius: '5px'
          }}
        >
          Pie Chart
        </button>
      </div>

      {renderGraph()}

      <div style={{
        marginTop: '20px',
        display: 'flex',
        gap: '10px'
      }}>
        <button 
          onClick={() => handleDownload('csv')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#4CAF50',
            color: 'white',
            border: 'none',
            borderRadius: '5px'
          }}
        >
          Download CSV
        </button>
        <button 
          onClick={() => handleDownload('json')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#FF9800',
            color: 'white',
            border: 'none',
            borderRadius: '5px'
          }}
        >
          Download JSON
        </button>
        <button 
          onClick={() => handleDownload('png')}
          style={{
            padding: '10px 20px',
            backgroundColor: '#2196F3',
            color: 'white',
            border: 'none',
            borderRadius: '5px'
          }}
        >
          Download PNG
        </button>
      </div>
    </div>
  );
}

export default GraphComponent;