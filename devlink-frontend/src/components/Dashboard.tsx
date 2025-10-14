import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import BusinessSearch from './BusinessSearch';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">DevLink</h1>
            <p className="text-sm text-gray-600">Connect with local businesses</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-600">
              Welcome, <span className="font-medium">{user?.username}</span>
            </div>
            <button
              onClick={logout}
              className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="py-8">
        <BusinessSearch />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-6xl mx-auto px-6 py-8 text-center text-gray-600">
          <p>&copy; 2025 DevLink. Made with ❤️ for developers seeking to connect with local businesses.</p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
