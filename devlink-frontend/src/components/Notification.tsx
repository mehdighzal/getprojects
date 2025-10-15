import React, { useEffect, useState } from 'react';

interface NotificationProps {
  message: string;
  type: 'error' | 'success' | 'info';
  onClose: () => void;
  duration?: number;
}

const Notification: React.FC<NotificationProps> = ({ 
  message, 
  type, 
  onClose, 
  duration = 5000 
}) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      setTimeout(onClose, 300); // Allow fade out animation
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const getStyles = () => {
    switch (type) {
      case 'error':
        return 'bg-red-100 border-red-400 text-red-700';
      case 'success':
        return 'bg-green-100 border-green-400 text-green-700';
      case 'info':
        return 'bg-blue-100 border-blue-400 text-blue-700';
      default:
        return 'bg-gray-100 border-gray-400 text-gray-700';
    }
  };

  if (!visible) return null;

  return (
    <div className={`fixed top-4 right-4 z-50 px-4 py-3 rounded border ${getStyles()} shadow-lg transition-opacity duration-300`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">{message}</span>
        <button
          onClick={() => {
            setVisible(false);
            setTimeout(onClose, 300);
          }}
          className="ml-3 text-lg leading-none hover:opacity-75"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default Notification;
