import axios from 'axios';

const API_BASE_URL = (process.env.REACT_APP_API_BASE_URL || 'http://172.19.32.147:8000') + '/api';

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
  business_country?: string;
  business_city?: string;
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
  
  updateProfile: (data: any) => {
    // Check if data is FormData (for file uploads)
    if (data instanceof FormData) {
      return api.put('/auth/profile/', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    }
    return api.put('/auth/profile/', data);
  },
  
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
    api.post('/emails/send/', emailData),
  history: (page: number, page_size = 10) =>
    api.get('/emails/history/', { params: { page, page_size } }),
  
  // Email Templates
  getTemplates: () => api.get('/emails/templates/'),
  createTemplate: (data: any) => api.post('/emails/templates/', data),
  updateTemplate: (id: number, data: any) => api.put(`/emails/templates/${id}/`, data),
  deleteTemplate: (id: number) => api.delete(`/emails/templates/${id}/`),
  
  // Bulk Campaigns
  getCampaigns: () => api.get('/emails/campaigns/'),
  createCampaign: (data: any) => api.post('/emails/campaigns/', data),
  updateCampaign: (id: number, data: any) => api.put(`/emails/campaigns/${id}/`, data),
  deleteCampaign: (id: number) => api.delete(`/emails/campaigns/${id}/`),
  sendCampaign: (id: number) => api.post(`/emails/campaigns/${id}/send/`),
  createCampaignFromBusinesses: (businesses: any[], name?: string) => 
    api.post('/emails/campaigns/create-from-businesses/', { businesses, name }),
  
  // Analytics
  getAnalytics: (days: number = 30) => api.get(`/emails/analytics/?days=${days}`),
  updateAnalytics: () => api.post('/emails/analytics/update/'),
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
