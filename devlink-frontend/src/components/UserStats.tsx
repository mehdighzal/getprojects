import React, { useState, useEffect } from 'react';
import { emailAPI, authAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

interface EmailStats {
  total_emails: number;
  emails_this_month: number;
  emails_this_week: number;
  unique_recipients: number;
  last_email_date?: string;
}

const UserStats: React.FC = () => {
  const [stats, setStats] = useState<EmailStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await authAPI.getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
      // Fallback to mock data if API fails
      const mockStats: EmailStats = {
        total_emails: 0,
        emails_this_month: 0,
        emails_this_week: 0,
        unique_recipients: 0,
        last_email_date: undefined,
      };
      setStats(mockStats);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner text="Loading statistics..." />;
  }

  if (!stats) {
    return (
      <div className="text-center py-8 text-gray-500">
        <p>Unable to load statistics</p>
      </div>
    );
  }

  const StatCard: React.FC<{ title: string; value: number; icon: string; color: string }> = ({ 
    title, 
    value, 
    icon, 
    color 
  }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-full ${color}`}>
          <span className="text-2xl">{icon}</span>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Activity</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Total Emails Sent"
            value={stats.total_emails}
            icon="📧"
            color="bg-blue-100 text-blue-600"
          />
          
          <StatCard
            title="This Month"
            value={stats.emails_this_month}
            icon="📅"
            color="bg-green-100 text-green-600"
          />
          
          <StatCard
            title="This Week"
            value={stats.emails_this_week}
            icon="📊"
            color="bg-yellow-100 text-yellow-600"
          />
          
          <StatCard
            title="Unique Recipients"
            value={stats.unique_recipients}
            icon="👥"
            color="bg-purple-100 text-purple-600"
          />
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h4>
        
        <div className="space-y-3">
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
              <span className="text-green-600 text-sm">✓</span>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Email sent successfully</p>
              <p className="text-xs text-gray-500">
                {stats.last_email_date ? new Date(stats.last_email_date).toLocaleString() : 'No recent activity'}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-blue-600 text-sm">🔍</span>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Business search completed</p>
              <p className="text-xs text-gray-500">Found 5 restaurants in Pisa, Italy</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
            <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
              <span className="text-purple-600 text-sm">🤖</span>
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">AI email generated</p>
              <p className="text-xs text-gray-500">Professional outreach email created</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h4>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="p-4 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">📧</div>
              <p className="text-sm font-medium text-gray-900">Send New Email</p>
              <p className="text-xs text-gray-500">Compose and send</p>
            </div>
          </button>

          <button className="p-4 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">🔍</div>
              <p className="text-sm font-medium text-gray-900">Search Businesses</p>
              <p className="text-xs text-gray-500">Find new contacts</p>
            </div>
          </button>

          <button className="p-4 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors">
            <div className="text-center">
              <div className="text-2xl mb-2">📊</div>
              <p className="text-sm font-medium text-gray-900">View Analytics</p>
              <p className="text-xs text-gray-500">See detailed stats</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default UserStats;
