import React, { useState, useEffect } from 'react';
import { emailAPI, aiAPI } from '../services/api';

interface Props {
  isOpen: boolean;
  defaultRecipient?: string;
  businessName?: string;
  businessCategory?: string;
  onClose: () => void;
}

const SendEmailModal: React.FC<Props> = ({ isOpen, defaultRecipient, businessName, businessCategory, onClose }) => {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [recipients, setRecipients] = useState<string>(defaultRecipient || '');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [developerName, setDeveloperName] = useState('');
  const [developerServices, setDeveloperServices] = useState('Web development and digital solutions');
  const [generating, setGenerating] = useState(false);

  // Update recipients when modal opens with new business
  useEffect(() => {
    if (isOpen && defaultRecipient) {
      setRecipients(defaultRecipient);
    } else if (!isOpen) {
      // Reset form when modal closes
      setRecipients('');
      setSubject('');
      setBody('');
      setError('');
      setSuccess('');
    }
  }, [isOpen, defaultRecipient]);

  if (!isOpen) return null;

  const parseRecipients = (value: string) =>
    value
      .split(',')
      .map(r => r.trim())
      .filter(r => r.length > 0);

  const onSubmit = async () => {
    setSending(true);
    setError('');
    setSuccess('');
    try {
      const list = parseRecipients(recipients);
      await emailAPI.sendEmail({ subject, body, recipients: list });
      setSuccess(`Sent to ${list.length} recipient(s)`);
      setSubject('');
      setBody('');
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to send email');
    } finally {
      setSending(false);
    }
  };

  const onGenerateAI = async () => {
    setError('');
    setSuccess('');
    setGenerating(true);
    try {
      const resp = await aiAPI.generateEmail({
        business_name: businessName || '',
        business_category: businessCategory || '',
        developer_name: developerName || 'Developer',
        developer_services: developerServices || 'Web development and digital solutions',
      });
      setSubject(resp.data.subject || '');
      setBody(resp.data.body || '');
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to generate with AI');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-full max-w-2xl p-6">
        <h3 className="text-xl font-semibold mb-4">Send Email</h3>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded mb-3">{error}</div>
        )}
        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-3 py-2 rounded mb-3">{success}</div>
        )}

        <div className="space-y-3">
          {/* AI generation helpers */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Developer name</label>
              <input
                type="text"
                value={developerName}
                onChange={(e) => setDeveloperName(e.target.value)}
                placeholder="Your name"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Developer services</label>
              <input
                type="text"
                value={developerServices}
                onChange={(e) => setDeveloperServices(e.target.value)}
                placeholder="e.g., Websites, apps, SEO"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="flex justify-end">
            <button
              type="button"
              onClick={onGenerateAI}
              className="px-3 py-2 text-sm rounded-md border border-blue-600 text-blue-700 hover:bg-blue-50 disabled:opacity-50"
              disabled={sending || generating}
            >
              {generating ? 'Generating…' : 'Generate with AI'}
            </button>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Recipients</label>
            <input
              type="text"
              value={recipients}
              onChange={(e) => setRecipients(e.target.value)}
              placeholder="Business email (auto-filled when you click Send Email)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Subject</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Body</label>
            <textarea
              value={body}
              onChange={(e) => setBody(e.target.value)}
              rows={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="mt-5 flex justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100"
            disabled={sending}
          >
            Close
          </button>
          <button
            onClick={onSubmit}
            disabled={sending}
            className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {sending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SendEmailModal;


