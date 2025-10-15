import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import BusinessSearch from './BusinessSearch';
import UserProfile from './UserProfile';
import UserStats from './UserStats';
import { emailAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [tab, setTab] = useState<'search' | 'history' | 'profile' | 'stats'>('search');
  const [history, setHistory] = useState<any[]>();
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const loadHistory = async () => {
    setLoading(true);
    try {
      const res = await emailAPI.history(page, pageSize);
      setHistory(res.data.results);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (tab === 'history') {
      loadHistory();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tab, page]);

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
        <div className="max-w-6xl mx-auto px-6">
          <div className="mb-6 flex space-x-3 overflow-x-auto">
            <button
              onClick={() => setTab('search')}
              className={`px-4 py-2 rounded-md whitespace-nowrap ${tab==='search' ? 'bg-blue-600 text-white' : 'bg-white border'}`}
            >
              🔍 Search
            </button>
            <button
              onClick={() => setTab('history')}
              className={`px-4 py-2 rounded-md whitespace-nowrap ${tab==='history' ? 'bg-blue-600 text-white' : 'bg-white border'}`}
            >
              📧 History
            </button>
            <button
              onClick={() => setTab('stats')}
              className={`px-4 py-2 rounded-md whitespace-nowrap ${tab==='stats' ? 'bg-blue-600 text-white' : 'bg-white border'}`}
            >
              📊 Stats
            </button>
            <button
              onClick={() => setTab('profile')}
              className={`px-4 py-2 rounded-md whitespace-nowrap ${tab==='profile' ? 'bg-blue-600 text-white' : 'bg-white border'}`}
            >
              👤 Profile
            </button>
          </div>

          {tab === 'search' && <BusinessSearch />}
          
          {tab === 'stats' && <UserStats />}
          
          {tab === 'profile' && <UserProfile />}

          {tab === 'history' && (
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b font-medium">Sent Emails</div>
              <div className="p-4">
                {loading ? (
                  <LoadingSpinner text="Loading email history..." />
                ) : history && history.length > 0 ? (
                  <div className="space-y-4">
                    {history.map((item) => (
                      <div key={item.id} className="border rounded p-3">
                        <div className="text-sm text-gray-500">{new Date(item.created_at).toLocaleString()}</div>
                        <div className="font-semibold">{item.subject}</div>
                        <div className="text-sm text-gray-700 whitespace-pre-wrap mt-1">{item.body}</div>
                        <div className="text-sm text-gray-600 mt-2">
                          To: {item.recipients.join(', ')}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <EmptyState
                    title="No emails sent yet"
                    description="Start by searching for businesses and sending your first email!"
                    icon="📧"
                    action={{
                      label: "Search Businesses",
                      onClick: () => setTab('search')
                    }}
                  />
                )}
              </div>
              <div className="p-4 border-t flex justify-between">
                <button disabled={page===1} onClick={() => setPage(p => Math.max(1, p-1))} className="px-3 py-1 border rounded disabled:opacity-50">Prev</button>
                <div>Page {page}</div>
                <button onClick={() => setPage(p => p+1)} className="px-3 py-1 border rounded">Next</button>
              </div>
            </div>
          )}
        </div>
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
