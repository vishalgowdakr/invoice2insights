'use client'
import { useAuthToken } from "@/app/_utils/auth_utils";
import AuthPage from "./auth/page";
import { useEffect, useState } from "react";
import App from "./dashboard/page";

export default function Home() {

  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    () => !!localStorage.getItem('accessToken')
  );
  const authToken = useAuthToken({ isAuthenticated, setIsAuthenticated });

  useEffect(() => {
    setIsAuthenticated(authToken.isAuthenticated);
    console.log('isAuthenticated', isAuthenticated)
  }, [authToken]);

  return (
    <div style={{ 'overflowX': 'hidden' }}>
      {
        isAuthenticated ? <App isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} /> : <AuthPage isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
      }
    </div>

  );
}
