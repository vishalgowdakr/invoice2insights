import React, { useState, ChangeEvent, FormEvent } from 'react';

interface SignupProps {
  onSignup: () => void;
  onSwitchToLogin: () => void;
}

function Signup({ onSignup, onSwitchToLogin }: SignupProps) {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    // TODO: Backend signup logic
    onSignup();
  };

  return (
    <div className="signup-container" style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      width: '100%',
      background: 'linear-gradient(135deg, #764ba2 0%, #667eea 100%)',
      padding: '20px',
      boxSizing: 'border-box',
      position: 'absolute',
      top: 0,
      left: 0,
    } as React.CSSProperties}>
      <form
        onSubmit={handleSubmit}
        style={{
          width: '380px',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          padding: '35px',
          borderRadius: '16px',
          boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
          // @ts-ignore - CSS custom properties for JSX pragma
          ':hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 15px 30px rgba(0, 0, 0, 0.2)'
          }
        } as any}
      >
        <h2 style={{
          textAlign: 'center',
          color: '#2d3748',
          marginBottom: '25px',
          fontSize: '24px',
          fontWeight: 600,
        }}>
          Create New Account
        </h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            // @ts-ignore - CSS custom properties for JSX pragma
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          } as any}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            // @ts-ignore - CSS custom properties for JSX pragma
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          } as any}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '20px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            // @ts-ignore - CSS custom properties for JSX pragma
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          } as any}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setConfirmPassword(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            marginBottom: '25px',
            border: '2px solid #e2e8f0',
            borderRadius: '8px',
            // @ts-ignore - CSS custom properties for JSX pragma
            ':focus': {
              borderColor: '#667eea',
              boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
            }
          } as any}
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
            // @ts-ignore - CSS custom properties for JSX pragma
            ':hover': {
              backgroundColor: '#5a67d8',
              transform: 'translateY(-1px)'
            },
            ':active': {
              transform: 'translateY(1px)'
            }
          } as any}
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
            // @ts-ignore - CSS custom properties for JSX pragma
            ':hover': {
              color: '#5a67d8',
              textDecoration: 'underline'
            }
          } as any}
        >
          Already have an account? Login
        </p>
      </form>
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
          }
          @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
          }
          input::placeholder { color: #a0aec0; }
          input:focus::placeholder { color: #718096; }
        `}
      </style>
    </div>
  );
}

export default Signup;
