import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Box, Typography, CircularProgress, Alert, Button } from '@mui/material';
import { templateAPI } from '../services/api';

const DigiKeyOAuthCallback: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');
  const [message, setMessage] = useState<string>('Processing OAuth callback...');

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const error = searchParams.get('error');
      const errorDescription = searchParams.get('error_description');

      if (error) {
        setStatus('error');
        setMessage(`OAuth Error: ${error}${errorDescription ? ` - ${errorDescription}` : ''}`);
        return;
      }

      if (!code) {
        setStatus('error');
        setMessage('No authorization code received from DigiKey');
        return;
      }

      try {
        // Send the authorization code to the backend for token exchange
        const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/template-sync/authenticate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            authorization_code: code
          })
        });

        const result = await response.json();

        if (response.ok) {
          setStatus('success');
          setMessage('Successfully authenticated with DigiKey API!');
          // Redirect to admin panel after 2 seconds
          setTimeout(() => {
            navigate('/admin');
          }, 2000);
        } else {
          setStatus('error');
          setMessage(`Authentication failed: ${result.detail || 'Unknown error'}`);
        }
      } catch (error) {
        console.error('OAuth callback error:', error);
        setStatus('error');
        setMessage('Failed to communicate with backend. Please check your connection.');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  const handleRetry = () => {
    setStatus('processing');
    setMessage('Processing OAuth callback...');
    // Trigger the effect again by updating a dependency
    window.location.reload();
  };

  const handleGoToAdmin = () => {
    navigate('/admin');
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: 3,
        textAlign: 'center'
      }}
    >
      {status === 'processing' && (
        <>
          <CircularProgress size={60} sx={{ mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            Authenticating with DigiKey
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {message}
          </Typography>
        </>
      )}

      {status === 'success' && (
        <>
          <Alert severity="success" sx={{ mb: 2, maxWidth: 500 }}>
            <Typography variant="h6" gutterBottom>
              Authentication Successful!
            </Typography>
            <Typography variant="body1">
              {message}
            </Typography>
          </Alert>
          <Typography variant="body2" color="text.secondary">
            Redirecting to admin panel...
          </Typography>
          <Button 
            variant="contained" 
            onClick={handleGoToAdmin}
            sx={{ mt: 2 }}
          >
            Go to Admin Panel Now
          </Button>
        </>
      )}

      {status === 'error' && (
        <>
          <Alert severity="error" sx={{ mb: 2, maxWidth: 500 }}>
            <Typography variant="h6" gutterBottom>
              Authentication Failed
            </Typography>
            <Typography variant="body1">
              {message}
            </Typography>
          </Alert>
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button variant="contained" onClick={handleRetry}>
              Retry
            </Button>
            <Button variant="outlined" onClick={handleGoToAdmin}>
              Go to Admin Panel
            </Button>
          </Box>
        </>
      )}
    </Box>
  );
};

export default DigiKeyOAuthCallback;