import React, { useState, useEffect } from 'react';
import { Business, aiAPI } from '../services/api';
import SendEmailModal from './SendEmailModal';
import BusinessCardSkeleton from './BusinessCardSkeleton';
import EmptyState from './EmptyState';
import LoadingSpinner from './LoadingSpinner';
import { useToast } from '../hooks/useToast';

const BusinessSearch: React.FC = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [emailOpen, setEmailOpen] = useState(false);
  const [emailRecipient, setEmailRecipient] = useState<string | undefined>(undefined);
  const { showSuccess, showError } = useToast();
  const [filters, setFilters] = useState({
    country: '',
    city: '',
    category: '',
    search: '',
  });

  const categories = [
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'club', label: 'Club' },
    { value: 'real_estate', label: 'Agenzia Immobiliare' },
    { value: 'travel_agency', label: 'Agenzia Viaggi' },
    { value: 'medical', label: 'Studio Medico' },
    { value: 'technical_studio', label: 'Studio Tecnico' },
    { value: 'dentist', label: 'Dentista' },
    { value: 'physiotherapist', label: 'Fisioterapista' },
    { value: 'private_school', label: 'Scuola Privata' },
    { value: 'beauty_center', label: 'Centro Estetico' },
    { value: 'artisan', label: 'Artigiano' },
    { value: 'other', label: 'Altro' },
  ];

  const searchBusinesses = async () => {
    setLoading(true);
    setError('');

    try {
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value !== '')
      );
      // Use Google Places API to get real businesses
      const response = await aiAPI.generateBusinesses(params);
      
      // Handle different response formats
      if (Array.isArray(response.data)) {
        setBusinesses(response.data as Business[]);
        if (response.data.length > 0) {
          showSuccess(`Found ${response.data.length} businesses!`);
        }
      } else if (response.data && Array.isArray(response.data.results)) {
        setBusinesses(response.data.results as Business[]);
        if (response.data.results.length > 0) {
          showSuccess(`Found ${response.data.results.length} businesses!`);
        }
      } else if (response.data && response.data.message) {
        setError(response.data.message);
        setBusinesses([]);
      } else {
        setBusinesses([]);
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.response?.data?.message || 'Failed to fetch businesses';
      setError(errorMessage);
      setBusinesses([]);
      showError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    searchBusinesses();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-800">
        Find Local Businesses
      </h2>

      {/* Search Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Country
            </label>
            <input
              type="text"
              value={filters.country}
              onChange={(e) => handleFilterChange('country', e.target.value)}
              placeholder="e.g., Italy"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              City
            </label>
            <input
              type="text"
              value={filters.city}
              onChange={(e) => handleFilterChange('city', e.target.value)}
              placeholder="e.g., Rome"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Categories</option>
              {categories.map(cat => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              placeholder="Search businesses..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          onClick={searchBusinesses}
          disabled={loading}
          className="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <LoadingSpinner size="sm" />
              <span>Searching...</span>
            </>
          ) : (
            <span>Search Businesses</span>
          )}
        </button>
      </div>

      {/* Info Banner */}
      {businesses.length > 0 && (
        <div className="bg-green-50 border border-green-300 text-green-800 px-4 py-3 rounded mb-4 text-sm">
          <strong>✅ Real Business Data:</strong> These are real businesses from Google Places API. 
          Contact information and addresses are verified from Google's database.
        </div>
      )}

      {/* No Results Info */}
      {!loading && businesses.length === 0 && !error && (
        <div className="bg-blue-50 border border-blue-300 text-blue-800 px-4 py-3 rounded mb-4 text-sm">
          <strong>ℹ️ No businesses found.</strong> This could mean:
          <ul className="list-disc ml-5 mt-2">
            <li>Google Places API key not configured (check backend console)</li>
            <li>No businesses match your search criteria</li>
            <li>API billing not enabled</li>
          </ul>
          <p className="mt-2">
            <strong>Setup Guide:</strong> See <code>GOOGLE_PLACES_SETUP.md</code> for instructions.
          </p>
        </div>
      )}

      {/* Results */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, index) => (
            <BusinessCardSkeleton key={index} />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && businesses.length === 0 && !error && (
        <EmptyState
          title="No businesses found"
          description="Try adjusting your search criteria or search in a different location."
          icon="🔍"
          action={{
            label: "Clear filters",
            onClick: () => {
              setFilters({ country: '', city: '', category: '', search: '' });
              searchBusinesses();
            }
          }}
        />
      )}

      {/* Results */}
      {!loading && businesses.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((business) => (
          <div key={business.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {business.name}
            </h3>
            
            <div className="space-y-2 text-sm text-gray-600">
              <p><span className="font-medium">Category:</span> {business.category}</p>
              <p><span className="font-medium">Location:</span> {business.city}, {business.country}</p>
              
              {business.email && (
                <p><span className="font-medium">Email:</span> 
                  <a href={`mailto:${business.email}`} className="text-blue-600 hover:text-blue-800 ml-1">
                    {business.email}
                  </a>
                </p>
              )}
              
              {business.phone && (
                <p><span className="font-medium">Phone:</span> {business.phone}</p>
              )}
              
              {business.website && (
                <p><span className="font-medium">Website:</span> 
                  <a href={business.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 ml-1">
                    Visit Website
                  </a>
                </p>
              )}
              
              {business.address && (
                <p><span className="font-medium">Address:</span> {business.address}</p>
              )}
            </div>

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => { setEmailRecipient(business.email); setEmailOpen(true); }}
                className="flex-1 bg-green-600 text-white py-2 px-3 rounded-md hover:bg-green-700 text-sm"
              >
                Generate Email
              </button>
              <button
                onClick={() => { setEmailRecipient(business.email); setEmailOpen(true); }}
                className="flex-1 bg-blue-600 text-white py-2 px-3 rounded-md hover:bg-blue-700 text-sm"
              >
                Send Email
              </button>
            </div>
          </div>
          ))}
        </div>
      )}

      <SendEmailModal
        isOpen={emailOpen}
        defaultRecipient={emailRecipient}
        businessName={businesses.find(b => b.email === emailRecipient)?.name}
        businessCategory={businesses.find(b => b.email === emailRecipient)?.category}
        onClose={() => setEmailOpen(false)}
      />
    </div>
  );
};

export default BusinessSearch;
