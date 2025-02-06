'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Login from './_components/Login';
import Signup from './_components/Signup';

interface AuthPageProps {
  isAuthenticated: boolean;
  setIsAuthenticated: React.Dispatch<React.SetStateAction<boolean>>;
}
const AuthPage = ({ isAuthenticated, setIsAuthenticated }: AuthPageProps) => {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);

  const handleSuccessfulAuth = () => {
    // Redirect to protected page after successful auth
    router.push('/');
  };

  return (
    <div className="auth-container">
      {isLogin ? (
        <Login
          onLogin={handleSuccessfulAuth}
          onSwitchToSignup={() => setIsLogin(false)}
          isAuthenticated={isAuthenticated}
          setIsAuthenticated={setIsAuthenticated}
        />
      ) : (
        <Signup
          onSignup={handleSuccessfulAuth}
          onSwitchToLogin={() => setIsLogin(true)}
        />
      )}
    </div>
  );
};

export default AuthPage;
