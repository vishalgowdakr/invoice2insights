import React, { useState } from 'react';

function Signup({ onSignup, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    // TODO: Backend signup logic
    // const response = await fetch('/api/signup', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ username, email, password })
    // });

    onSignup();
  };

  return (
    <div className="signup-container" style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      height: '100%',  // Ensures full height coverage
      width: '100%',  // Ensures full width coverage
      background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
      padding: '20px',
      boxSizing: 'border-box',
      transition: 'background 0.3s ease-in-out',
      position: 'absolute', // Makes sure it takes up the full screen space
      top: 0,
      left: 0,
      right: 0,
      bottom: 0
    }}>
      <form 
        onSubmit={handleSubmit}
        style={{
          width: '380px',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '35px',
          borderRadius: '16px',
          boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
          backdropFilter: 'blur(10px)',
          transform: 'translateY(0)',
          transition: 'all 0.3s ease-in-out',
          animation: 'fadeIn 0.5s ease-out',
          ':hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 15px 30px rgba(0, 0, 0, 0.2)'
          }
        }}
      >
        <h2 style={{
          textAlign: 'center',
          color: '#2d3748',
          marginBottom: '25px',
          fontSize: '24px',
          fontWeight: '600',
          animation: 'slideDown 0.5s ease-out'
        }}>
          Create New Account
        </h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            fontSize: '16px',
            transition: 'all 0.2s ease-in-out',
            outline: 'none',
            backgroundColor: 'white',
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          }}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            fontSize: '16px',
            transition: 'all 0.2s ease-in-out',
            outline: 'none',
            backgroundColor: 'white',
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          }}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            fontSize: '16px',
            transition: 'all 0.2s ease-in-out',
            outline: 'none',
            backgroundColor: 'white',
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          }}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '25px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            fontSize: '16px',
            transition: 'all 0.2s ease-in-out',
            outline: 'none',
            backgroundColor: 'white',
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          }}
          required
        />
        <button
          type="submit"
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: '500',
            transition: 'all 0.2s ease-in-out',
            ':hover': {
              backgroundColor: '#5a67d8',
              transform: 'translateY(-1px)'
            },
            ':active': {
              transform: 'translateY(1px)'
            }
          }}
        >
          Sign Up
        </button>
        <p
          onClick={onSwitchToLogin}
          style={{
            textAlign: 'center',
            marginTop: '20px',
            color: '#667eea',
            cursor: 'pointer',
            fontSize: '15px',
            transition: 'color 0.2s ease-in-out',
            ':hover': {
              color: '#5a67d8',
              textDecoration: 'underline'
            }
          }}
        >
          Already have an account? Login
        </p>
      </form>
      <style>
        {`
          @keyframes fadeIn {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          
          @keyframes slideDown {
            from {
              opacity: 0;
              transform: translateY(-20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          
          input::placeholder {
            color: #a0aec0;
          }
          
          input:focus::placeholder {
            color: #718096;
          }
        `}
      </style>
    </div>
  );
}

export default Signup;
