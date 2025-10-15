import axios from 'axios';

const API_BASE_URL = (process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000') + '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear it
      localStorage.removeItem('token');
      console.log('Token expired, please login again');
      
      // Dispatch a custom event that AuthContext can listen to
      window.dispatchEvent(new CustomEvent('tokenExpired'));
    }
    return Promise.reject(error);
  }
);

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Business {
  id: number;
  name: string;
  email: string;
  phone: string;
  website: string;
  category: string;
  country: string;
  city: string;
  address: string;
  created_at: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface EmailRequest {
  subject: string;
  body: string;
  recipients: string[];
}

export interface GenerateEmailRequest {
  business_name: string;
  business_category: string;
  developer_name: string;
  developer_services: string;
}

export const authAPI = {
  register: (username: string, email: string, password: string) =>
    api.post('/auth/register/', { username, email, password }),
  
  login: (username: string, password: string) =>
    api.post('/auth/login/', { username, password }),
  
  getMe: () => api.get('/auth/me/'),
  
  getProfile: () => api.get('/auth/profile/'),
  
  updateProfile: (data: any) => api.put('/auth/profile/', data),
  
  changePassword: (currentPassword: string, newPassword: string, confirmPassword: string) =>
    api.post('/auth/change-password/', { 
      current_password: currentPassword, 
      new_password: newPassword, 
      confirm_password: confirmPassword 
    }),
  
  getStats: () => api.get('/auth/stats/'),
};

export const businessAPI = {
  getBusinesses: (params?: { country?: string; city?: string; category?: string; search?: string }) =>
    api.get('/businesses/', { params }),
  
  createBusiness: (business: Partial<Business>) =>
    api.post('/businesses/', business),
};

export const emailAPI = {
  sendEmail: (emailData: EmailRequest) =>
    api.post('/email/send/', emailData),
  history: (page: number, page_size = 10) =>
    api.get('/email/history/', { params: { page, page_size } }),
};

export const aiAPI = {
  generateEmail: (data: GenerateEmailRequest) =>
    api.post('/ai/generate-email/', data),
  
  generateBulkEmail: (data: { category: string; developer_name: string; developer_services: string }) =>
    api.post('/ai/generate-bulk-email/', data),

  generateBusinesses: (filters: { country?: string; city?: string; category?: string; search?: string }) =>
    api.post('/ai/generate-businesses/', filters),
};

export default api;
