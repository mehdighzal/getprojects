import React from 'react';

const BusinessCardSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 animate-pulse">
      {/* Business name skeleton */}
      <div className="h-6 bg-gray-200 rounded mb-3 w-3/4"></div>
      
      {/* Category skeleton */}
      <div className="h-4 bg-gray-200 rounded mb-2 w-1/2"></div>
      
      {/* Location skeleton */}
      <div className="h-4 bg-gray-200 rounded mb-2 w-2/3"></div>
      
      {/* Email skeleton */}
      <div className="h-4 bg-gray-200 rounded mb-2 w-4/5"></div>
      
      {/* Phone skeleton */}
      <div className="h-4 bg-gray-200 rounded mb-2 w-1/3"></div>
      
      {/* Address skeleton */}
      <div className="h-4 bg-gray-200 rounded mb-4 w-full"></div>
      
      {/* Buttons skeleton */}
      <div className="flex space-x-2">
        <div className="h-8 bg-gray-200 rounded w-24"></div>
        <div className="h-8 bg-gray-200 rounded w-20"></div>
      </div>
    </div>
  );
};

export default BusinessCardSkeleton;
