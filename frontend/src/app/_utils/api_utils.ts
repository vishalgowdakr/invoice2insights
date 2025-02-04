// Django API Communication Utilities

/**
 * Configuration for API communication
 */
const API_BASE_URL: string = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/';

/**
 * Helper function to handle common error responses
 */
async function handleResponse(response: Response): Promise<any> {
  if (!response.ok) {
    const errorBody: string = await response.text();
    throw new Error(`HTTP error! status: ${response.status}, message: ${errorBody}`);
  }

  const contentType: string | null = response.headers.get('content-type');
  if (contentType?.includes('application/json')) {
    return response.json();
  }
  return response.text();
}

/**
 * Utility for making unauthorized GET requests
 */
export async function getUnAuthorized(endpoint: string, params: Record<string, any> = {}): Promise<any> {
  const url: URL = new URL(`${API_BASE_URL}${endpoint}`);

  Object.keys(params).forEach(key =>
    url.searchParams.append(key, params[key])
  );

  try {
    const response: Response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    return handleResponse(response);
  } catch (error) {
    console.error('Unauthorized GET request failed:', error);
    throw error;
  }
}

/**
 * Utility for making unauthorized POST requests
 */
export async function postUnAuthorized(endpoint: string, data: any): Promise<any> {
  try {
    const response: Response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return handleResponse(response);
  } catch (error) {
    console.error('Unauthorized POST request failed:', error);
    throw error;
  }
}

/**
 * Utility for making authorized GET requests
 */
export async function getAuthorized(endpoint: string, params: Record<string, any> = {}): Promise<any> {
  const url: URL = new URL(`${API_BASE_URL}${endpoint}`);

  Object.keys(params).forEach(key =>
    url.searchParams.append(key, params[key])
  );

  try {
    const token: string | null = localStorage.getItem('accessToken');
    if (!token) throw new Error('No access token found');

    const response: Response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    return handleResponse(response);
  } catch (error) {
    console.error('Authorized GET request failed:', error);
    throw error;
  }
}

/**
 * Utility for making authorized POST requests
 */
export async function postAuthorized(
  endpoint: string,
  data: any,
  contentType: string = 'application/json'
): Promise<any> {
  try {
    const token: string | null = localStorage.getItem('accessToken');
    if (!token) throw new Error('No access token found');

    const response: Response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': contentType
      },
      body: contentType === 'multipart/form-data' ? data : JSON.stringify(data)
    });
    return handleResponse(response);
  } catch (error) {
    console.error('Authorized POST request failed:', error);
    throw error;
  }
}

/**
 * Utility for making authorized PUT requests
 */
export async function putAuthorized(
  endpoint: string,
  data: any,
  contentType: string = 'application/json'
): Promise<any> {
  try {
    const token: string | null = localStorage.getItem('accessToken');
    if (!token) throw new Error('No access token found');

    const headers: Record<string, string> = {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json'
    };

    if (contentType !== 'multipart/form-data') {
      headers['Content-Type'] = contentType;
    }

    const response: Response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers,
      body: contentType === 'multipart/form-data' ? data : JSON.stringify(data)
    });

    return handleResponse(response);
  } catch (error) {
    console.error('Authorized PUT request failed:', error);
    throw error;
  }
}

/**
 * Utility for making authorized DELETE requests
 */
export async function deleteAuthorized(endpoint: string): Promise<any> {
  try {
    const token: string | null = localStorage.getItem('accessToken');
    if (!token) throw new Error('No access token found');

    const response: Response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    return handleResponse(response);
  } catch (error) {
    console.error('Authorized DELETE request failed:', error);
    throw error;
  }
}

/**
 * Refresh access token utility
 */
export async function refreshToken(): Promise<string> {
  try {
    const refreshToken: string | null = localStorage.getItem('refreshToken');
    if (!refreshToken) throw new Error('No refresh token found');

    const response: Response = await fetch(`${API_BASE_URL}/token/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ refresh: refreshToken })
    });

    const data: any = await handleResponse(response);
    localStorage.setItem('accessToken', data.access);
    return data.access;
  } catch (error) {
    console.error('Token refresh failed:', error);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    throw error;
  }
}

/**
 * Logout utility to clear tokens
 */
export function logout(): void {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
}
