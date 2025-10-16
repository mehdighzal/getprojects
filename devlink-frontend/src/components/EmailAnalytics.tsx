import React, { useState, useEffect } from 'react';
import { emailAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import LoadingSpinner from './LoadingSpinner';

interface AnalyticsData {
  date_range: {
    start_date: string;
    end_date: string;
    days: number;
  };
  summary: {
    total_emails: number;
    total_campaigns: number;
    templates_count: number;
  };
  analytics: Array<{
    id: number;
    date: string;
    emails_sent: number;
    unique_recipients: number;
    templates_used: number;
    campaigns_completed: number;
  }>;
  top_templates: Array<{
    name: string;
    usage_count: number;
  }>;
  status_breakdown: Array<{
    status: string;
    count: number;
  }>;
}

const EmailAnalytics: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDays, setSelectedDays] = useState(30);
  const { showError } = useToast();

  useEffect(() => {
    loadAnalytics();
  }, [selectedDays]);

  const loadAnalytics = async () => {
    try {
      const response = await emailAPI.getAnalytics(selectedDays);
      setAnalytics(response.data);
    } catch (error: any) {
      showError('Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'sent': return 'text-green-600';
      case 'failed': return 'text-red-600';
      case 'pending': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  if (loading) {
    return <LoadingSpinner text="Loading analytics..." />;
  }

  if (!analytics) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Email Analytics</h2>
        <p className="text-gray-600">No analytics data available.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Email Analytics</h2>
        <div className="flex items-center space-x-2">
          <label className="text-sm text-gray-700">Period:</label>
          <select
            value={selectedDays}
            onChange={(e) => setSelectedDays(Number(e.target.value))}
            className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-blue-600">Total Emails</p>
              <p className="text-2xl font-bold text-blue-900">{analytics.summary.total_emails}</p>
            </div>
          </div>
        </div>

        <div className="bg-green-50 rounded-lg p-4">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-green-600">Campaigns</p>
              <p className="text-2xl font-bold text-green-900">{analytics.summary.total_campaigns}</p>
            </div>
          </div>
        </div>

        <div className="bg-purple-50 rounded-lg p-4">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-purple-600">Templates</p>
              <p className="text-2xl font-bold text-purple-900">{analytics.summary.templates_count}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Email Status Breakdown */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-4">Email Status Breakdown</h3>
          <div className="space-y-3">
            {analytics.status_breakdown.map((item, index) => (
              <div key={index} className="flex justify-between items-center">
                <span className={`font-medium ${getStatusColor(item.status)}`}>
                  {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                </span>
                <span className="text-gray-600">{item.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top Templates */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-4">Most Used Templates</h3>
          {analytics.top_templates.length === 0 ? (
            <p className="text-gray-500 text-sm">No template usage data available.</p>
          ) : (
            <div className="space-y-3">
              {analytics.top_templates.map((template, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="font-medium text-gray-700">{template.name}</span>
                  <span className="text-gray-600">{template.usage_count} uses</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Daily Analytics Chart */}
      {analytics.analytics.length > 0 && (
        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-4">Daily Email Activity</h3>
          <div className="space-y-2">
            {analytics.analytics.slice(0, 10).map((day, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {new Date(day.date).toLocaleDateString()}
                </span>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-600">{day.emails_sent} emails</span>
                  <div className="w-20 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ 
                        width: `${Math.min(100, (day.emails_sent / Math.max(...analytics.analytics.map(d => d.emails_sent))) * 100)}%` 
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Date Range Info */}
      <div className="mt-6 text-sm text-gray-500 text-center">
        Showing data from {new Date(analytics.date_range.start_date).toLocaleDateString()} to{' '}
        {new Date(analytics.date_range.end_date).toLocaleDateString()} ({analytics.date_range.days} days)
      </div>
    </div>
  );
};

export default EmailAnalytics;
