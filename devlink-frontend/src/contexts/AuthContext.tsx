import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, authAPI } from '../services/api';

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
  sessionExpired: boolean;
  clearSessionExpired: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [sessionExpired, setSessionExpired] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authAPI.getMe()
        .then(response => {
          setUser(response.data);
        })
        .catch((error) => {
          // Handle token expiration or invalid tokens
          if (error.response?.status === 401) {
            console.log('Token expired or invalid, clearing token');
            localStorage.removeItem('token');
            setUser(null);
            setSessionExpired(true);
          }
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }

    // Listen for token expiration events from API interceptor
    const handleTokenExpired = () => {
      setUser(null);
      setSessionExpired(true);
    };

    window.addEventListener('tokenExpired', handleTokenExpired);
    return () => window.removeEventListener('tokenExpired', handleTokenExpired);
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authAPI.login(username, password);
    const { access } = response.data;
    localStorage.setItem('token', access);
    
    const userResponse = await authAPI.getMe();
    setUser(userResponse.data);
  };

  const register = async (username: string, email: string, password: string) => {
    await authAPI.register(username, email, password);
    await login(username, password);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setSessionExpired(false);
  };

  const clearSessionExpired = () => {
    setSessionExpired(false);
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
    sessionExpired,
    clearSessionExpired,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
