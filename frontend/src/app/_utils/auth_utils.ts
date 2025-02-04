interface DecodedToken {
  exp: number;
}

interface AuthTokenHook {
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (access: string, refresh: string) => void;
  logout: () => void;
  rotateToken: () => Promise<string | null>;
  withTokenRotation: <T extends (...args: any[]) => Promise<any>>(apiCall: T) => T;
  isTokenExpired: (token: string) => boolean;
  getAccessToken: () => string | null;
  getRefreshToken: () => string | null;
}

export const useAuthToken = ({ isAuthenticated, setIsAuthenticated }: any): AuthTokenHook => {


  const decodeToken = (token: string): DecodedToken | null => {
    if (!token) return null;
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(window.atob(base64));
    } catch (error) {
      console.error('Token decoding failed:', error);
      return null;
    }
  };

  const isTokenExpired = (token: string): boolean => {
    const decoded = decodeToken(token);
    if (!decoded) return true;
    return decoded.exp * 1000 < Date.now();
  };

  const rotateToken = async (): Promise<string | null> => {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      logout();
      return null;
    }

    try {
      const response = await fetch('/api/token/refresh/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      if (!response.ok) throw new Error('Token refresh failed');

      const data: { access: string; refresh?: string } = await response.json();
      localStorage.setItem('accessToken', data.access);

      if (data.refresh) {
        localStorage.setItem('refreshToken', data.refresh);
      }

      setIsAuthenticated(true);
      return data.access;
    } catch (error) {
      console.error('Token rotation failed:', error);
      logout();
      return null;
    }
  };

  const logout = (): void => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setIsAuthenticated(false);
  };

  const login = (access: string, refresh: string): void => {
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    setIsAuthenticated(true);
  };

  const getAccessToken = (): string | null => localStorage.getItem('accessToken');
  const getRefreshToken = (): string | null => localStorage.getItem('refreshToken');

  const withTokenRotation = <T extends (...args: any[]) => Promise<any>>(apiCall: T): T => {
    return (async (...args: Parameters<T>): Promise<ReturnType<T>> => {
      const currentToken = getAccessToken();
      if (currentToken && isTokenExpired(currentToken)) {
        const newToken = await rotateToken();
        if (!newToken) throw new Error('Unable to refresh token');
      }
      return apiCall(...args);
    }) as T;
  };

  return {
    accessToken: getAccessToken(),
    refreshToken: getRefreshToken(),
    isAuthenticated,
    login,
    logout,
    rotateToken,
    withTokenRotation,
    isTokenExpired,
    getAccessToken,
    getRefreshToken
  };
};
