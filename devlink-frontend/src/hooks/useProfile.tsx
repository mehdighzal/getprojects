import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { authAPI } from '../services/api';

export interface UserProfileData {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  date_joined: string;
  last_login?: string;
  profile?: {
    bio?: string;
    github_url?: string;
    website_url?: string;
    linkedin_url?: string;
    twitter_url?: string;
    work_image?: string;
    company?: string;
    job_title?: string;
    location?: string;
    phone?: string;
    created_at?: string;
    updated_at?: string;
  };
}

export const useProfile = () => {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      setError(null);
      const response = await authAPI.getProfile();
      setProfileData(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load profile');
      console.error('Failed to load profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshProfile = () => {
    loadProfile();
  };

  // Load profile when user changes
  useEffect(() => {
    loadProfile();
  }, [user]);

  // Helper functions to get profile information
  const getDeveloperName = () => {
    if (!profileData) return user?.username || '';
    
    const { first_name, last_name, username } = profileData;
    if (first_name && last_name) {
      return `${first_name} ${last_name}`;
    }
    if (first_name) {
      return first_name;
    }
    return username;
  };

  const getFullName = () => {
    if (!profileData) return '';
    
    const { first_name, last_name } = profileData;
    if (first_name && last_name) {
      return `${first_name} ${last_name}`;
    }
    if (first_name) {
      return first_name;
    }
    return '';
  };

  const getProfileImage = () => {
    return profileData?.profile?.work_image || null;
  };

  const getBio = () => {
    return profileData?.profile?.bio || '';
  };

  const getCompany = () => {
    return profileData?.profile?.company || '';
  };

  const getJobTitle = () => {
    return profileData?.profile?.job_title || '';
  };

  const getLocation = () => {
    return profileData?.profile?.location || '';
  };

  const getPhone = () => {
    return profileData?.profile?.phone || '';
  };

  const getSocialLinks = () => {
    if (!profileData?.profile) return {};
    
    return {
      github: profileData.profile.github_url || '',
      website: profileData.profile.website_url || '',
      linkedin: profileData.profile.linkedin_url || '',
      twitter: profileData.profile.twitter_url || '',
    };
  };

  const getProfessionalInfo = () => {
    if (!profileData?.profile) return '';
    
    const { job_title, company } = profileData.profile;
    if (job_title && company) {
      return `${job_title} at ${company}`;
    }
    if (job_title) {
      return job_title;
    }
    if (company) {
      return company;
    }
    return '';
  };

  return {
    profileData,
    loading,
    error,
    refreshProfile,
    // Helper functions
    getDeveloperName,
    getFullName,
    getProfileImage,
    getBio,
    getCompany,
    getJobTitle,
    getLocation,
    getPhone,
    getSocialLinks,
    getProfessionalInfo,
  };
};
