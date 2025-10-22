import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useToast } from '../hooks/useToast';
import LoadingSpinner from './LoadingSpinner';
import api from '../services/api';

interface GmailStatus {
  connected: boolean;
  email: string | null;
  token_valid: boolean;
}

const GmailIntegration: React.FC = () => {
  const { user } = useAuth();
  const { showSuccess, showError } = useToast();
  const [gmailStatus, setGmailStatus] = useState<GmailStatus>({
    connected: false,
    email: null,
    token_valid: false
  });
  const [loading, setLoading] = useState(false);
  const [connecting, setConnecting] = useState(false);

  // Check Gmail status on component mount
  useEffect(() => {
    checkGmailStatus();
  }, []);

  const checkGmailStatus = async () => {
    try {
      const response = await api.get('/emails/gmail/status/');
      console.log('Gmail status response:', response.data);
      setGmailStatus(response.data);
    } catch (error) {
      console.error('Error checking Gmail status:', error);
      // Set default status on error
      setGmailStatus({
        connected: false,
        email: null,
        token_valid: false
      });
    }
  };

  const connectGmail = async () => {
    setConnecting(true);
    try {
      const response = await api.get('/emails/gmail/auth-url/');
      const data = response.data;
      
      // Open Gmail authorization in a new window
      const authWindow = window.open(data.auth_url, 'gmail-auth', 'width=500,height=600');
      
      // Listen for the callback
      const checkClosed = setInterval(() => {
        if (authWindow?.closed) {
          clearInterval(checkClosed);
          setConnecting(false);
          // Check status after window closes
          setTimeout(checkGmailStatus, 1000);
        }
      }, 1000);
      
      // Also listen for messages from the popup
      const handleMessage = (event: MessageEvent) => {
        if (event.origin !== window.location.origin) return;
        if (event.data.type === 'GMAIL_CONNECTED') {
          clearInterval(checkClosed);
          setConnecting(false);
          checkGmailStatus();
        }
      };
      
      window.addEventListener('message', handleMessage);
      
      // Clean up event listener when component unmounts or window closes
      const cleanup = () => {
        window.removeEventListener('message', handleMessage);
        clearInterval(checkClosed);
      };
      
      // Set up cleanup
      setTimeout(cleanup, 30000); // Clean up after 30 seconds
    } catch (error: any) {
      console.error('Error connecting Gmail:', error);
      const errorMessage = error.response?.data?.error || 'Failed to connect Gmail';
      
      if (errorMessage.includes('GMAIL_CLIENT_ID not configured')) {
        showError('Gmail integration is not configured. Please contact your administrator to set up Gmail OAuth2 credentials.');
      } else {
        showError(errorMessage);
      }
      setConnecting(false);
    }
  };

  const disconnectGmail = async () => {
    setLoading(true);
    try {
      await api.post('/emails/gmail/disconnect/');
      showSuccess('Gmail disconnected successfully');
      setGmailStatus({
        connected: false,
        email: null,
        token_valid: false
      });
    } catch (error: any) {
      console.error('Error disconnecting Gmail:', error);
      showError(error.response?.data?.error || 'Failed to disconnect Gmail');
    } finally {
      setLoading(false);
    }
  };

  const testGmailConnection = async () => {
    setLoading(true);
    try {
      const response = await api.post('/emails/gmail/send/', {
        subject: 'Test Email from DevLink',
        body: 'This is a test email to verify your Gmail integration is working correctly.',
        recipients: [user?.email || 'test@example.com']
      });

      const data = response.data;
      showSuccess(`Test email sent successfully! Gmail Message ID: ${data.gmail_message_id}`);
    } catch (error: any) {
      console.error('Error sending test email:', error);
      showError(error.response?.data?.error || 'Failed to send test email');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Gmail Integration</h3>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${gmailStatus.connected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-600">
            {gmailStatus.connected ? 'Connected' : 'Not Connected'}
          </span>
        </div>
      </div>

      {gmailStatus.connected ? (
        <div className="space-y-4">
          <div className="p-4 bg-green-50 border border-green-200 rounded-md">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <div>
                <h4 className="font-medium text-green-900">Gmail Connected</h4>
                <p className="text-sm text-green-700">
                  Connected as: {gmailStatus.email}
                </p>
                <p className="text-sm text-green-700">
                  Token Status: {gmailStatus.token_valid ? 'Valid' : 'Expired'}
                </p>
              </div>
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={testGmailConnection}
              disabled={loading || !gmailStatus.token_valid}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {loading && <LoadingSpinner size="sm" />}
              <span>Send Test Email</span>
            </button>

            <button
              onClick={disconnectGmail}
              disabled={loading}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 flex items-center space-x-2"
            >
              {loading && <LoadingSpinner size="sm" />}
              <span>Disconnect</span>
            </button>
          </div>

          {!gmailStatus.token_valid && (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
              <div className="flex items-center">
                <svg className="w-5 h-5 text-yellow-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <div>
                  <h4 className="font-medium text-yellow-900">Token Expired</h4>
                  <p className="text-sm text-yellow-700">
                    Your Gmail access token has expired. Please reconnect to continue using Gmail integration.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-md">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-gray-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
              <div>
                <h4 className="font-medium text-gray-900">Gmail Not Connected</h4>
                <p className="text-sm text-gray-700">
                  Connect your Gmail account to send emails using your real Gmail address.
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={connectGmail}
            disabled={connecting}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
          >
            {connecting && <LoadingSpinner size="sm" />}
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-.904.732-1.636 1.636-1.636h3.819v9.273L12 8.954l6.545 4.14V3.821h3.819A1.636 1.636 0 0 1 24 5.457z"/>
            </svg>
            <span>{connecting ? 'Connecting...' : 'Connect Gmail'}</span>
          </button>
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <h4 className="font-medium text-blue-900 mb-2">How it works:</h4>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>• Connect your Gmail account using OAuth2 for secure authentication</li>
          <li>• Send emails using your real Gmail address instead of system emails</li>
          <li>• Tokens are stored securely and automatically refreshed when needed</li>
          <li>• You can disconnect at any time to revoke access</li>
        </ul>
      </div>

      <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
        <h4 className="font-medium text-yellow-900 mb-2">Setup Required:</h4>
        <p className="text-sm text-yellow-700">
          To use Gmail integration, your administrator needs to configure Gmail OAuth2 credentials. 
          See the Gmail OAuth2 Setup Guide for detailed instructions.
        </p>
      </div>
    </div>
  );
};

export default GmailIntegration;
