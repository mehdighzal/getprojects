import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ToastProvider } from './contexts/ToastContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import Notification from './components/Notification';
import ToastContainer from './components/ToastContainer';
import PWAInstallPrompt from './components/PWAInstallPrompt';
import ManualInstallButton from './components/ManualInstallButton';

const AppContent: React.FC = () => {
  const { user, loading, sessionExpired, clearSessionExpired } = useAuth();
  const [isRegistering, setIsRegistering] = useState(false);

  // Register service worker
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
          .then((registration) => {
            console.log('SW registered: ', registration);
          })
          .catch((registrationError) => {
            console.log('SW registration failed: ', registrationError);
          });
      });
    }
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <>
        <Dashboard />
        <ToastContainer />
        <PWAInstallPrompt />
        <ManualInstallButton />
      </>
    );
  }

  return (
    <>
      {sessionExpired && (
        <Notification
          message="Your session has expired. Please login again."
          type="error"
          onClose={clearSessionExpired}
          duration={8000}
        />
      )}
      
      <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">DevLink</h1>
            <p className="text-gray-600">Connect developers with local businesses</p>
          </div>
          
          {isRegistering ? (
            <RegisterForm onSwitchToLogin={() => setIsRegistering(false)} />
          ) : (
            <LoginForm onSwitchToRegister={() => setIsRegistering(true)} />
          )}
        </div>
      </div>
      <ToastContainer />
      <PWAInstallPrompt />
      <ManualInstallButton />
    </>
  );
};

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <AppContent />
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
