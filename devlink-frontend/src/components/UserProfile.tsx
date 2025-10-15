import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import LoadingSpinner from './LoadingSpinner';

interface UserProfileData {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  date_joined: string;
  last_login?: string;
}

const UserProfile: React.FC = () => {
  const { user, logout } = useAuth();
  const { showSuccess, showError } = useToast();
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });

  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username,
        email: user.email,
        first_name: '',
        last_name: '',
      });
      setProfileData({
        id: user.id,
        username: user.username,
        email: user.email,
        date_joined: new Date().toISOString(),
        last_login: new Date().toISOString(),
      });
    }
  }, [user]);

  const handleSave = async () => {
    setLoading(true);
    try {
      await authAPI.updateProfile(formData);
      showSuccess('Profile updated successfully!');
      setEditing(false);
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async () => {
    const currentPassword = prompt('Enter current password:');
    const newPassword = prompt('Enter new password:');
    const confirmPassword = prompt('Confirm new password:');

    if (!currentPassword || !newPassword || !confirmPassword) {
      showError('All fields are required');
      return;
    }

    if (newPassword !== confirmPassword) {
      showError('New passwords do not match');
      return;
    }

    if (newPassword.length < 8) {
      showError('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);
    try {
      await authAPI.changePassword(currentPassword, newPassword, confirmPassword);
      showSuccess('Password changed successfully!');
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  if (!user || !profileData) {
    return <LoadingSpinner text="Loading profile..." />;
  }

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{user.username}</h2>
            <p className="text-gray-600">{user.email}</p>
            <p className="text-sm text-gray-500">
              Member since {new Date(profileData.date_joined).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* Account Information */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Account Information</h3>
          <button
            onClick={() => setEditing(!editing)}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            {editing ? 'Cancel' : 'Edit'}
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          {editing && (
            <div className="flex space-x-3">
              <button
                onClick={handleSave}
                disabled={loading}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center space-x-2"
              >
                {loading && <LoadingSpinner size="sm" />}
                <span>Save Changes</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Security Settings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Security</h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 border border-gray-200 rounded-md">
            <div>
              <h4 className="font-medium text-gray-900">Password</h4>
              <p className="text-sm text-gray-600">Last changed: Never</p>
            </div>
            <button
              onClick={handleChangePassword}
              disabled={loading}
              className="px-4 py-2 text-sm bg-yellow-600 text-white rounded-md hover:bg-yellow-700 disabled:opacity-50"
            >
              Change Password
            </button>
          </div>

          <div className="flex justify-between items-center p-4 border border-gray-200 rounded-md">
            <div>
              <h4 className="font-medium text-gray-900">Two-Factor Authentication</h4>
              <p className="text-sm text-gray-600">Add an extra layer of security</p>
            </div>
            <button
              disabled
              className="px-4 py-2 text-sm bg-gray-400 text-white rounded-md cursor-not-allowed"
            >
              Coming Soon
            </button>
          </div>
        </div>
      </div>

      {/* Account Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Actions</h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 border border-red-200 rounded-md bg-red-50">
            <div>
              <h4 className="font-medium text-red-900">Delete Account</h4>
              <p className="text-sm text-red-700">Permanently delete your account and all data</p>
            </div>
            <button
              disabled
              className="px-4 py-2 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50 cursor-not-allowed"
            >
              Coming Soon
            </button>
          </div>

          <div className="flex justify-between items-center p-4 border border-gray-200 rounded-md">
            <div>
              <h4 className="font-medium text-gray-900">Export Data</h4>
              <p className="text-sm text-gray-600">Download all your data</p>
            </div>
            <button
              disabled
              className="px-4 py-2 text-sm bg-gray-400 text-white rounded-md cursor-not-allowed"
            >
              Coming Soon
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
