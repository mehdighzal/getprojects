import React, { useState, useEffect } from 'react';
import { emailAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';

interface BulkEmailCampaign {
  id: number;
  name: string;
  subject: string;
  body: string;
  recipients: any[];
  status: 'draft' | 'sending' | 'completed' | 'failed';
  sent_count: number;
  total_count: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  template_name?: string;
}

const BulkEmailCampaigns: React.FC = () => {
  const [campaigns, setCampaigns] = useState<BulkEmailCampaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCampaign, setEditingCampaign] = useState<BulkEmailCampaign | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    subject: '',
    body: '',
    recipients: [] as any[]
  });
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const response = await emailAPI.getCampaigns();
      setCampaigns(response.data);
    } catch (error: any) {
      showError('Failed to load campaigns');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingCampaign) {
        await emailAPI.updateCampaign(editingCampaign.id, formData);
        showSuccess('Campaign updated successfully!');
      } else {
        await emailAPI.createCampaign(formData);
        showSuccess('Campaign created successfully!');
      }
      setShowModal(false);
      setEditingCampaign(null);
      setFormData({ name: '', subject: '', body: '', recipients: [] });
      loadCampaigns();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to save campaign');
    }
  };

  const handleEdit = (campaign: BulkEmailCampaign) => {
    setEditingCampaign(campaign);
    setFormData({
      name: campaign.name,
      subject: campaign.subject,
      body: campaign.body,
      recipients: campaign.recipients
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this campaign?')) {
      try {
        await emailAPI.deleteCampaign(id);
        showSuccess('Campaign deleted successfully!');
        loadCampaigns();
      } catch (error: any) {
        showError('Failed to delete campaign');
      }
    }
  };

  const handleSendCampaign = async (id: number) => {
    if (window.confirm('Are you sure you want to send this campaign? This action cannot be undone.')) {
      try {
        await emailAPI.sendCampaign(id);
        showSuccess('Campaign sending started!');
        loadCampaigns();
      } catch (error: any) {
        showError('Failed to start campaign');
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'draft': return 'bg-gray-100 text-gray-800';
      case 'sending': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getProgressPercentage = (campaign: BulkEmailCampaign) => {
    if (campaign.total_count === 0) return 0;
    return Math.round((campaign.sent_count / campaign.total_count) * 100);
  };

  if (loading) {
    return <LoadingSpinner text="Loading campaigns..." />;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Bulk Email Campaigns</h2>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          + New Campaign
        </button>
      </div>

      {campaigns.length === 0 ? (
        <EmptyState
          title="No campaigns yet"
          description="Create your first bulk email campaign to reach multiple businesses at once."
          icon="📢"
          action={{
            label: "Create Campaign",
            onClick: () => setShowModal(true)
          }}
        />
      ) : (
        <div className="space-y-4">
          {campaigns.map((campaign) => (
            <div key={campaign.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-lg">{campaign.name}</h3>
                  <p className="text-sm text-gray-600">Subject: {campaign.subject}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(campaign.status)}`}>
                  {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
                </span>
              </div>

              {campaign.status === 'sending' && (
                <div className="mb-3">
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{campaign.sent_count} / {campaign.total_count}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${getProgressPercentage(campaign)}%` }}
                    ></div>
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                <div>
                  <span className="font-medium">Recipients:</span> {campaign.recipients.length}
                </div>
                <div>
                  <span className="font-medium">Sent:</span> {campaign.sent_count}
                </div>
                <div>
                  <span className="font-medium">AI Generation:</span> 
                  <span className="ml-1 px-2 py-1 rounded text-xs bg-purple-100 text-purple-800">
                    🤖 Personalized
                  </span>
                </div>
                <div>
                  <span className="font-medium">Created:</span> {new Date(campaign.created_at).toLocaleDateString()}
                </div>
                {campaign.completed_at && (
                  <div>
                    <span className="font-medium">Completed:</span> {new Date(campaign.completed_at).toLocaleDateString()}
                  </div>
                )}
              </div>

              <div className="flex space-x-2">
                {campaign.status === 'draft' && (
                  <button
                    onClick={() => handleSendCampaign(campaign.id)}
                    className="bg-green-600 text-white py-1 px-3 rounded text-sm hover:bg-green-700 flex items-center space-x-1"
                  >
                    <span>🤖</span>
                    <span>Send AI Campaign</span>
                  </button>
                )}
                {campaign.status === 'draft' && (
                  <button
                    onClick={() => handleEdit(campaign)}
                    className="bg-blue-600 text-white py-1 px-3 rounded text-sm hover:bg-blue-700"
                  >
                    Edit
                  </button>
                )}
                {campaign.status === 'draft' && (
                  <button
                    onClick={() => handleDelete(campaign.id)}
                    className="bg-red-600 text-white py-1 px-3 rounded text-sm hover:bg-red-700"
                  >
                    Delete
                  </button>
                )}
                <button
                  onClick={() => {
                    // View campaign details
                    alert(`Campaign: ${campaign.name}\nRecipients: ${campaign.recipients.length}\nStatus: ${campaign.status}`);
                  }}
                  className="bg-gray-600 text-white py-1 px-3 rounded text-sm hover:bg-gray-700"
                >
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Campaign Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">
              {editingCampaign ? 'Edit Campaign' : 'Create New Campaign'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Campaign Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email Body</label>
                <textarea
                  value={formData.body}
                  onChange={(e) => setFormData({ ...formData, body: e.target.value })}
                  rows={8}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Recipients ({formData.recipients.length} businesses)
                </label>
                <div className="border rounded-md p-3 bg-gray-50 max-h-32 overflow-y-auto">
                  {formData.recipients.length === 0 ? (
                    <p className="text-gray-500 text-sm">No recipients added yet. Use the business search to add recipients.</p>
                  ) : (
                    formData.recipients.map((recipient, index) => (
                      <div key={index} className="text-sm text-gray-700">
                        {recipient.name} - {recipient.email}
                      </div>
                    ))
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Note: Add recipients by searching for businesses and selecting them for bulk campaigns.
                </p>
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
                >
                  {editingCampaign ? 'Update Campaign' : 'Create Campaign'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingCampaign(null);
                    setFormData({ name: '', subject: '', body: '', recipients: [] });
                  }}
                  className="flex-1 bg-gray-300 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default BulkEmailCampaigns;
