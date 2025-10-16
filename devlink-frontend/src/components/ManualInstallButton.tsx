import React, { useState, useEffect } from 'react';
import { useToast } from '../hooks/useToast';

const ManualInstallButton: React.FC = () => {
  const [showManualInstall, setShowManualInstall] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [isAndroid, setIsAndroid] = useState(false);
  const { showSuccess } = useToast();

  useEffect(() => {
    // Detect device type
    const userAgent = navigator.userAgent.toLowerCase();
    setIsIOS(/iphone|ipad|ipod/.test(userAgent));
    setIsAndroid(/android/.test(userAgent));

    // Check if app is already installed
    const isInstalled = window.matchMedia('(display-mode: standalone)').matches || 
                       (window.navigator as any).standalone === true;

    // Show manual install instructions if:
    // 1. Not already installed
    // 2. On mobile device
    // 3. Haven't seen the automatic prompt
    if (!isInstalled && (isIOS || isAndroid)) {
      // Show after a delay to allow automatic prompt to appear first
      const timer = setTimeout(() => {
        setShowManualInstall(true);
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, []);

  const handleInstallClick = () => {
    if (isIOS) {
      showSuccess('Tap the Share button and select "Add to Home Screen"');
    } else if (isAndroid) {
      showSuccess('Tap the menu (⋮) and select "Add to Home Screen"');
    }
  };

  if (!showManualInstall) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 z-40">
      <button
        onClick={handleInstallClick}
        className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
        title="Install App"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
  );
};

export default ManualInstallButton;
