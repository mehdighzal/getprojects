import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import BusinessSearch from '../BusinessSearch';
import { ToastProvider } from '../../contexts/ToastContext';

// Mock the API
jest.mock('../../services/api', () => ({
  aiAPI: {
    generateBusinesses: jest.fn(),
  },
}));

// Mock the useToast hook
jest.mock('../../hooks/useToast', () => ({
  useToast: () => ({
    showSuccess: jest.fn(),
    showError: jest.fn(),
  }),
}));

const mockBusinesses = [
  {
    id: 1,
    name: 'Test Restaurant',
    email: 'test@restaurant.com',
    phone: '+39 050 123456',
    website: 'https://testrestaurant.com',
    category: 'restaurant',
    country: 'Italy',
    city: 'Pisa',
    address: 'Via Test, 123, Pisa',
    rating: 4.5,
    user_ratings_total: 100,
  },
];

const renderWithToastProvider = (component: React.ReactElement) => {
  return render(
    <ToastProvider>
      {component}
    </ToastProvider>
  );
};

describe('BusinessSearch Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders search form with all input fields', () => {
    renderWithToastProvider(<BusinessSearch />);
    
    expect(screen.getByLabelText(/country/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/city/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/search/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /search businesses/i })).toBeInTheDocument();
  });

  test('allows user to input search criteria', () => {
    renderWithToastProvider(<BusinessSearch />);
    
    const countryInput = screen.getByLabelText(/country/i);
    const cityInput = screen.getByLabelText(/city/i);
    const searchInput = screen.getByLabelText(/search/i);
    
    fireEvent.change(countryInput, { target: { value: 'Italy' } });
    fireEvent.change(cityInput, { target: { value: 'Pisa' } });
    fireEvent.change(searchInput, { target: { value: 'restaurant' } });
    
    expect(countryInput).toHaveValue('Italy');
    expect(cityInput).toHaveValue('Pisa');
    expect(searchInput).toHaveValue('restaurant');
  });

  test('shows loading state when searching', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateBusinesses.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: mockBusinesses }), 100))
    );

    renderWithToastProvider(<BusinessSearch />);
    
    const searchButton = screen.getByRole('button', { name: /search businesses/i });
    fireEvent.click(searchButton);
    
    expect(screen.getByText(/searching/i)).toBeInTheDocument();
    expect(searchButton).toBeDisabled();
  });

  test('displays businesses when search is successful', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateBusinesses.mockResolvedValue({ data: mockBusinesses });

    renderWithToastProvider(<BusinessSearch />);
    
    const searchButton = screen.getByRole('button', { name: /search businesses/i });
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText('Test Restaurant')).toBeInTheDocument();
      expect(screen.getByText('test@restaurant.com')).toBeInTheDocument();
      expect(screen.getByText('Via Test, 123, Pisa')).toBeInTheDocument();
    });
  });

  test('shows empty state when no businesses found', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateBusinesses.mockResolvedValue({ data: [] });

    renderWithToastProvider(<BusinessSearch />);
    
    const searchButton = screen.getByRole('button', { name: /search businesses/i });
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText(/no businesses found/i)).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateBusinesses.mockRejectedValue(new Error('API Error'));

    renderWithToastProvider(<BusinessSearch />);
    
    const searchButton = screen.getByRole('button', { name: /search businesses/i });
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText(/no businesses found/i)).toBeInTheDocument();
    });
  });

  test('has generate email and send email buttons for each business', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateBusinesses.mockResolvedValue({ data: mockBusinesses });

    renderWithToastProvider(<BusinessSearch />);
    
    const searchButton = screen.getByRole('button', { name: /search businesses/i });
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getAllByText(/generate email/i)).toHaveLength(1);
      expect(screen.getAllByText(/send email/i)).toHaveLength(1);
    });
  });
});
