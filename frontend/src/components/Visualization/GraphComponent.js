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

  const COLORS = ['#6366f1', '#22c55e', '#eab308', '#ec4899', '#8b5cf6'];

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
            <Bar dataKey="revenue" fill="#6366f1" />
            <Bar dataKey="cost" fill="#22c55e" />
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
              fill="#6366f1"
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
    console.log(`Downloading in ${format} format`);
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '2rem',
      margin:'50px',
      backgroundColor: '#f8fafc',
      borderRadius: '1rem',
      boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
      transition: 'all 0.3s ease',
      ':hover': {
        boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)'
      }
    }}>
      <div style={{
        marginBottom: '1.5rem',
        display: 'flex',
        gap: '0.75rem'
      }}>
        <button 
          onClick={() => setGraphType('bar')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: graphType === 'bar' ? '#6366f1' : 'transparent',
            color: graphType === 'bar' ? '#ffffff' : '#6366f1',
            border: '2px solid #6366f1',
            borderRadius: '0.5rem',
            fontWeight: '600',
            transition: 'all 0.2s ease',
            cursor: 'pointer',
            ':hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 6px -1px rgb(99 102 241 / 0.2)'
            }
          }}
        >
          Bar Graph
        </button>
        <button 
          onClick={() => setGraphType('pie')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: graphType === 'pie' ? '#6366f1' : 'transparent',
            color: graphType === 'pie' ? '#ffffff' : '#6366f1',
            border: '2px solid #6366f1',
            borderRadius: '0.5rem',
            fontWeight: '600',
            transition: 'all 0.2s ease',
            cursor: 'pointer',
            ':hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 4px 6px -1px rgb(99 102 241 / 0.2)'
            }
          }}
        >
          Pie Chart
        </button>
      </div>

      <div style={{
        transform: 'scale(1)',
        transition: 'transform 0.3s ease',
        ':hover': {
          transform: 'scale(1.02)'
        }
      }}>
        {renderGraph()}
      </div>

      <div style={{
        marginTop: '1.5rem',
        display: 'flex',
        gap: '0.75rem'
      }}>
        <button 
          onClick={() => handleDownload('csv')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#22c55e',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            ':hover': {
              transform: 'translateY(-2px)',
              backgroundColor: '#16a34a',
              boxShadow: '0 4px 6px -1px rgb(34 197 94 / 0.2)'
            }
          }}
        >
          Download CSV
        </button>
        <button 
          onClick={() => handleDownload('json')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#eab308',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            ':hover': {
              transform: 'translateY(-2px)',
              backgroundColor: '#ca8a04',
              boxShadow: '0 4px 6px -1px rgb(234 179 8 / 0.2)'
            }
          }}
        >
          Download JSON
        </button>
        <button 
          onClick={() => handleDownload('png')}
          style={{
            padding: '0.75rem 1.5rem',
            backgroundColor: '#6366f1',
            color: 'white',
            border: 'none',
            borderRadius: '0.5rem',
            fontWeight: '600',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            ':hover': {
              transform: 'translateY(-2px)',
              backgroundColor: '#4f46e5',
              boxShadow: '0 4px 6px -1px rgb(99 102 241 / 0.2)'
            }
          }}
        >
          Download PNG
        </button>
      </div>
    </div>
  );
}

export default GraphComponent;