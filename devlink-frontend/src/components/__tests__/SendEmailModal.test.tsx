import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SendEmailModal from '../SendEmailModal';
import { ToastProvider } from '../../contexts/ToastContext';

// Mock the API
jest.mock('../../services/api', () => ({
  emailAPI: {
    sendEmail: jest.fn(),
  },
  aiAPI: {
    generateEmail: jest.fn(),
  },
}));

// Mock the useToast hook
jest.mock('../../hooks/useToast', () => ({
  useToast: () => ({
    showSuccess: jest.fn(),
    showError: jest.fn(),
  }),
}));

const renderWithToastProvider = (component: React.ReactElement) => {
  return render(
    <ToastProvider>
      {component}
    </ToastProvider>
  );
};

describe('SendEmailModal Component', () => {
  const defaultProps = {
    isOpen: true,
    onClose: jest.fn(),
    defaultRecipient: 'test@business.com',
    businessName: 'Test Business',
    businessCategory: 'restaurant',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders modal when open', () => {
    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    expect(screen.getByText(/send email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/recipients/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/subject/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/body/i)).toBeInTheDocument();
  });

  test('does not render when closed', () => {
    renderWithToastProvider(<SendEmailModal {...defaultProps} isOpen={false} />);
    
    expect(screen.queryByText(/send email/i)).not.toBeInTheDocument();
  });

  test('pre-fills recipient email', () => {
    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    const recipientInput = screen.getByLabelText(/recipients/i);
    expect(recipientInput).toHaveValue('test@business.com');
  });

  test('allows user to edit email fields', () => {
    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    const subjectInput = screen.getByLabelText(/subject/i);
    const bodyInput = screen.getByLabelText(/body/i);
    
    fireEvent.change(subjectInput, { target: { value: 'Test Subject' } });
    fireEvent.change(bodyInput, { target: { value: 'Test Body' } });
    
    expect(subjectInput).toHaveValue('Test Subject');
    expect(bodyInput).toHaveValue('Test Body');
  });

  test('sends email successfully', async () => {
    const { emailAPI } = require('../../services/api');
    emailAPI.sendEmail.mockResolvedValue({ data: { success: true } });

    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    const subjectInput = screen.getByLabelText(/subject/i);
    const bodyInput = screen.getByLabelText(/body/i);
    const sendButton = screen.getByRole('button', { name: /send email/i });
    
    fireEvent.change(subjectInput, { target: { value: 'Test Subject' } });
    fireEvent.change(bodyInput, { target: { value: 'Test Body' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(emailAPI.sendEmail).toHaveBeenCalledWith({
        subject: 'Test Subject',
        body: 'Test Body',
        recipients: ['test@business.com'],
      });
    });
  });

  test('generates email with AI', async () => {
    const { aiAPI } = require('../../services/api');
    aiAPI.generateEmail.mockResolvedValue({
      data: {
        subject: 'AI Generated Subject',
        body: 'AI Generated Body',
      },
    });

    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    const generateButton = screen.getByRole('button', { name: /generate with ai/i });
    fireEvent.click(generateButton);
    
    await waitFor(() => {
      expect(aiAPI.generateEmail).toHaveBeenCalledWith({
        business_name: 'Test Business',
        business_category: 'restaurant',
        developer_name: '',
        developer_services: 'Web development and digital solutions',
      });
    });
  });

  test('shows loading state when sending email', async () => {
    const { emailAPI } = require('../../services/api');
    emailAPI.sendEmail.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({ data: { success: true } }), 100))
    );

    renderWithToastProvider(<SendEmailModal {...defaultProps} />);
    
    const subjectInput = screen.getByLabelText(/subject/i);
    const bodyInput = screen.getByLabelText(/body/i);
    const sendButton = screen.getByRole('button', { name: /send email/i });
    
    fireEvent.change(subjectInput, { target: { value: 'Test Subject' } });
    fireEvent.change(bodyInput, { target: { value: 'Test Body' } });
    fireEvent.click(sendButton);
    
    expect(screen.getByText(/sending/i)).toBeInTheDocument();
    expect(sendButton).toBeDisabled();
  });

  test('closes modal when close button is clicked', () => {
    const onClose = jest.fn();
    renderWithToastProvider(<SendEmailModal {...defaultProps} onClose={onClose} />);
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    fireEvent.click(closeButton);
    
    expect(onClose).toHaveBeenCalled();
  });
});
