import React, { useEffect, useState } from 'react';
import { Alert, Button, Box, Typography } from '@mui/material';
import { templateAPI } from '../services/api';

interface SSLHelperProps {
  children: React.ReactNode;
}

const SSLCertificateHelper: React.FC<SSLHelperProps> = ({ children }) => {
  const [sslError, setSSLError] = useState<string | null>(null);
  const [isChecking, setIsChecking] = useState(true);

  const checkSSLConnection = async () => {
    try {
      setIsChecking(true);
      await templateAPI.getPanelTemplates();
      setSSLError(null);
    } catch (error: any) {
      console.log('SSL Check Error:', error);
      if (error.code === 'ERR_CERT_AUTHORITY_INVALID' || 
          error.code === 'ERR_CERT_COMMON_NAME_INVALID' ||
          error.message?.includes('certificate') ||
          error.message?.includes('SSL') ||
          error.message?.includes('ERR_CERT') ||
          error.message?.includes('NET::ERR_CERT')) {
        setSSLError('SSL certificate validation failed');
      } else if (error.message?.includes('Network Error') || error.code === 'ERR_NETWORK') {
        setSSLError('Network connection failed - likely SSL certificate issue');
      }
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkSSLConnection();
  }, []);

  const handleAcceptCertificate = () => {
    const backendUrl = process.env.REACT_APP_API_BASE_URL?.replace('/api', '') || 'https://localhost:8001';
    window.open(backendUrl, '_blank');
  };

  const handleRetryConnection = () => {
    checkSSLConnection();
  };

  if (isChecking) {
    return (
      <Box sx={{ p: 2 }}>
        <Typography>Checking backend connection...</Typography>
      </Box>
    );
  }

  if (sslError) {
    return (
      <Box sx={{ p: 2, maxWidth: 800, mx: 'auto' }}>
        <Alert severity="warning" sx={{ mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            SSL Certificate Issue Detected
          </Typography>
          <Typography gutterBottom>
            The backend is running with a self-signed SSL certificate that needs to be accepted by your browser.
          </Typography>
          <Typography gutterBottom>
            <strong>To fix this:</strong>
          </Typography>
          <ol>
            <li>Click "Accept Certificate" below to open the backend URL in a new tab</li>
            <li>You'll see a security warning - click "Advanced" then "Proceed to localhost (unsafe)"</li>
            <li>Close the new tab and click "Retry Connection" below</li>
          </ol>
          
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleAcceptCertificate}
            >
              Accept Certificate
            </Button>
            <Button 
              variant="outlined" 
              onClick={handleRetryConnection}
            >
              Retry Connection
            </Button>
          </Box>
        </Alert>
      </Box>
    );
  }

  return <>{children}</>;
};

export default SSLCertificateHelper;