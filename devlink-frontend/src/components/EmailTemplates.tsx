import React, { useState, useEffect } from 'react';
import { emailAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';

interface EmailTemplate {
  id: number;
  name: string;
  subject: string;
  body: string;
  category: string;
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

const EmailTemplates: React.FC = () => {
  const [templates, setTemplates] = useState<EmailTemplate[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<EmailTemplate | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    subject: '',
    body: '',
    category: 'general',
    is_default: false
  });
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await emailAPI.getTemplates();
      setTemplates(response.data);
    } catch (error: any) {
      showError('Failed to load templates');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingTemplate) {
        await emailAPI.updateTemplate(editingTemplate.id, formData);
        showSuccess('Template updated successfully!');
      } else {
        await emailAPI.createTemplate(formData);
        showSuccess('Template created successfully!');
      }
      setShowModal(false);
      setEditingTemplate(null);
      setFormData({ name: '', subject: '', body: '', category: 'general', is_default: false });
      loadTemplates();
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to save template');
    }
  };

  const handleEdit = (template: EmailTemplate) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      subject: template.subject,
      body: template.body,
      category: template.category,
      is_default: template.is_default
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      try {
        await emailAPI.deleteTemplate(id);
        showSuccess('Template deleted successfully!');
        loadTemplates();
      } catch (error: any) {
        showError('Failed to delete template');
      }
    }
  };

  const handleUseTemplate = (template: EmailTemplate) => {
    // This would be used when composing emails
    showSuccess(`Template "${template.name}" selected for use`);
  };

  if (loading) {
    return <LoadingSpinner text="Loading templates..." />;
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Email Templates</h2>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          + New Template
        </button>
      </div>

      {templates.length === 0 ? (
        <EmptyState
          title="No templates yet"
          description="Create your first email template to save time when composing emails."
          icon="📧"
          action={{
            label: "Create Template",
            onClick: () => setShowModal(true)
          }}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => (
            <div key={template.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-lg">{template.name}</h3>
                {template.is_default && (
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Default</span>
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">Category: {template.category}</p>
              <p className="text-sm font-medium mb-1">Subject: {template.subject}</p>
              <p className="text-sm text-gray-700 mb-4 line-clamp-3">{template.body}</p>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleUseTemplate(template)}
                  className="flex-1 bg-green-600 text-white py-1 px-3 rounded text-sm hover:bg-green-700"
                >
                  Use
                </button>
                <button
                  onClick={() => handleEdit(template)}
                  className="flex-1 bg-blue-600 text-white py-1 px-3 rounded text-sm hover:bg-blue-700"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(template.id)}
                  className="flex-1 bg-red-600 text-white py-1 px-3 rounded text-sm hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Template Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">
              {editingTemplate ? 'Edit Template' : 'Create New Template'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Template Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="general">General</option>
                  <option value="introduction">Introduction</option>
                  <option value="follow-up">Follow-up</option>
                  <option value="proposal">Proposal</option>
                  <option value="thank-you">Thank You</option>
                </select>
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
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="is_default"
                  checked={formData.is_default}
                  onChange={(e) => setFormData({ ...formData, is_default: e.target.checked })}
                  className="mr-2"
                />
                <label htmlFor="is_default" className="text-sm text-gray-700">
                  Set as default template
                </label>
              </div>
              <div className="flex space-x-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
                >
                  {editingTemplate ? 'Update Template' : 'Create Template'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingTemplate(null);
                    setFormData({ name: '', subject: '', body: '', category: 'general', is_default: false });
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

export default EmailTemplates;
