import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../services/api';
import { useToast } from '../hooks/useToast';
import { useProfile, UserProfileData } from '../hooks/useProfile';
import LoadingSpinner from './LoadingSpinner';

const UserProfile: React.FC = () => {
  const { user, logout } = useAuth();
  const { showSuccess, showError } = useToast();
  const { profileData, loading: profileLoading, refreshProfile } = useProfile();
  const [loading, setLoading] = useState(false);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    profile: {
      bio: '',
      github_url: '',
      website_url: '',
      linkedin_url: '',
      twitter_url: '',
      company: '',
      job_title: '',
      location: '',
      phone: '',
    }
  });
  const [workImage, setWorkImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Update form data when profile data changes
  useEffect(() => {
    if (profileData) {
      setFormData({
        username: profileData.username || '',
        email: profileData.email || '',
        first_name: profileData.first_name || '',
        last_name: profileData.last_name || '',
        profile: {
          bio: profileData.profile?.bio || '',
          github_url: profileData.profile?.github_url || '',
          website_url: profileData.profile?.website_url || '',
          linkedin_url: profileData.profile?.linkedin_url || '',
          twitter_url: profileData.profile?.twitter_url || '',
          company: profileData.profile?.company || '',
          job_title: profileData.profile?.job_title || '',
          location: profileData.profile?.location || '',
          phone: profileData.profile?.phone || '',
        }
      });
      if (profileData.profile?.work_image) {
        setImagePreview(profileData.profile.work_image);
      }
    } else if (user) {
      // Fallback to basic user data
      setFormData({
        username: user.username,
        email: user.email,
        first_name: '',
        last_name: '',
        profile: {
          bio: '',
          github_url: '',
          website_url: '',
          linkedin_url: '',
          twitter_url: '',
          company: '',
          job_title: '',
          location: '',
          phone: '',
        }
      });
    }
  }, [profileData, user]);

  const handleInputChange = (field: string, value: string) => {
    if (field.startsWith('profile.')) {
      const profileField = field.replace('profile.', '');
      setFormData(prev => ({
        ...prev,
        profile: {
          ...prev.profile,
          [profileField]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }));
    }
  };

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setWorkImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const formDataToSend = new FormData();
      
      // Add user fields
      formDataToSend.append('username', formData.username);
      formDataToSend.append('email', formData.email);
      formDataToSend.append('first_name', formData.first_name);
      formDataToSend.append('last_name', formData.last_name);
      
      // Add profile fields
      Object.entries(formData.profile).forEach(([key, value]) => {
        formDataToSend.append(`profile.${key}`, value);
      });
      
      // Add image if selected
      if (workImage) {
        formDataToSend.append('profile.work_image', workImage);
      }

      await authAPI.updateProfile(formDataToSend);
      showSuccess('Profile updated successfully!');
      setEditing(false);
      
      // Refresh profile data using the hook
      refreshProfile();
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

  if (!user || profileLoading) {
    return <LoadingSpinner text="Loading profile..." />;
  }

  return (
    <div className="space-y-6">
      {/* Profile Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center space-x-4">
          <div className="relative">
            {imagePreview ? (
              <img
                src={imagePreview}
                alt="Profile"
                className="w-16 h-16 rounded-full object-cover"
              />
            ) : (
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                {user.username.charAt(0).toUpperCase()}
              </div>
            )}
            {editing && (
              <label className="absolute -bottom-1 -right-1 bg-blue-600 text-white rounded-full p-1 cursor-pointer hover:bg-blue-700">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </label>
            )}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {formData.first_name && formData.last_name 
                ? `${formData.first_name} ${formData.last_name}` 
                : user.username}
            </h2>
            <p className="text-gray-600">{user.email}</p>
            {formData.profile.job_title && formData.profile.company && (
              <p className="text-sm text-gray-500">
                {formData.profile.job_title} at {formData.profile.company}
              </p>
            )}
            <p className="text-sm text-gray-500">
              Member since {profileData ? new Date(profileData.date_joined).toLocaleDateString() : 'Unknown'}
            </p>
          </div>
        </div>
      </div>

      {/* Basic Information */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Basic Information</h3>
          <button
            onClick={() => setEditing(!editing)}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            {editing ? 'Cancel' : 'Edit'}
          </button>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => handleInputChange('first_name', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => handleInputChange('last_name', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
              <input
                type="tel"
                value={formData.profile.phone}
                onChange={(e) => handleInputChange('profile.phone', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
              <input
                type="text"
                value={formData.profile.location}
                onChange={(e) => handleInputChange('profile.location', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
            <textarea
              value={formData.profile.bio}
              onChange={(e) => handleInputChange('profile.bio', e.target.value)}
              disabled={!editing}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="Tell us about yourself..."
            />
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

      {/* Professional Information */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Professional Information</h3>
        
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
              <input
                type="text"
                value={formData.profile.job_title}
                onChange={(e) => handleInputChange('profile.job_title', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                placeholder="e.g., Software Developer"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
              <input
                type="text"
                value={formData.profile.company}
                onChange={(e) => handleInputChange('profile.company', e.target.value)}
                disabled={!editing}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
                placeholder="e.g., Tech Corp"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Social Links */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Social Links</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">GitHub</label>
            <input
              type="url"
              value={formData.profile.github_url}
              onChange={(e) => handleInputChange('profile.github_url', e.target.value)}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="https://github.com/username"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
            <input
              type="url"
              value={formData.profile.website_url}
              onChange={(e) => handleInputChange('profile.website_url', e.target.value)}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="https://yourwebsite.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn</label>
            <input
              type="url"
              value={formData.profile.linkedin_url}
              onChange={(e) => handleInputChange('profile.linkedin_url', e.target.value)}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="https://linkedin.com/in/username"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Twitter</label>
            <input
              type="url"
              value={formData.profile.twitter_url}
              onChange={(e) => handleInputChange('profile.twitter_url', e.target.value)}
              disabled={!editing}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              placeholder="https://twitter.com/username"
            />
          </div>
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