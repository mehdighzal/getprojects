import React, { useState, useEffect } from 'react';
import { Business, aiAPI, emailAPI } from '../services/api';
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
  const [selectedBusinesses, setSelectedBusinesses] = useState<Set<number>>(new Set());
  const [bulkCampaignLoading, setBulkCampaignLoading] = useState(false);
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

  const handleBusinessSelect = (businessId: number) => {
    const newSelected = new Set(selectedBusinesses);
    if (newSelected.has(businessId)) {
      newSelected.delete(businessId);
    } else {
      newSelected.add(businessId);
    }
    setSelectedBusinesses(newSelected);
  };

  const handleSelectAll = () => {
    if (selectedBusinesses.size === businesses.length) {
      setSelectedBusinesses(new Set());
    } else {
      setSelectedBusinesses(new Set(businesses.map(b => b.id)));
    }
  };

  const createBulkCampaign = async () => {
    if (selectedBusinesses.size === 0) {
      showError('Please select at least one business');
      return;
    }

    setBulkCampaignLoading(true);
    try {
      const selectedBusinessData = businesses.filter(b => selectedBusinesses.has(b.id));
      const campaignName = prompt('Enter campaign name:', `AI Bulk Campaign - ${new Date().toLocaleDateString()}`);
      
      if (!campaignName) return;

      await emailAPI.createCampaignFromBusinesses(selectedBusinessData, campaignName);
      showSuccess(`Bulk campaign created with ${selectedBusinesses.size} businesses! Check the Campaigns tab to send.`);
      setSelectedBusinesses(new Set());
    } catch (error: any) {
      showError(error.response?.data?.detail || 'Failed to create bulk campaign');
    } finally {
      setBulkCampaignLoading(false);
    }
  };

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

             <div className="mt-4 flex space-x-3">
               <button
                 onClick={searchBusinesses}
                 disabled={loading}
                 className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 flex items-center justify-center space-x-2"
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
               
               {businesses.length > 0 && (
                 <button
                   onClick={createBulkCampaign}
                   disabled={bulkCampaignLoading || selectedBusinesses.size === 0}
                   className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 flex items-center space-x-2"
                 >
                   {bulkCampaignLoading ? (
                     <>
                       <LoadingSpinner size="sm" />
                       <span>Creating...</span>
                     </>
                   ) : (
                     <>
                       <span>🤖 AI Bulk Campaign</span>
                       {selectedBusinesses.size > 0 && (
                         <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                           {selectedBusinesses.size}
                         </span>
                       )}
                     </>
                   )}
                 </button>
               )}
             </div>
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

      {/* Selection Controls */}
      {!loading && businesses.length > 0 && (
        <div className="mb-4 flex items-center justify-between bg-gray-50 p-3 rounded-lg">
          <div className="flex items-center space-x-3">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={selectedBusinesses.size === businesses.length && businesses.length > 0}
                onChange={handleSelectAll}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-gray-700">
                Select All ({selectedBusinesses.size}/{businesses.length})
              </span>
            </label>
          </div>
          {selectedBusinesses.size > 0 && (
            <div className="text-sm text-gray-600">
              {selectedBusinesses.size} business{selectedBusinesses.size !== 1 ? 'es' : ''} selected
            </div>
          )}
        </div>
      )}

      {/* Results */}
      {!loading && businesses.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {businesses.map((business) => (
          <div 
            key={business.id} 
            className={`bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border-2 ${
              selectedBusinesses.has(business.id) ? 'border-blue-500 bg-blue-50' : 'border-transparent'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  {business.name}
                </h3>
              </div>
              <label className="flex items-center cursor-pointer ml-2">
                <input
                  type="checkbox"
                  checked={selectedBusinesses.has(business.id)}
                  onChange={() => handleBusinessSelect(business.id)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
              </label>
            </div>
            
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
