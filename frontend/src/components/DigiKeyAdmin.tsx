import React, { useState, useEffect } from 'react';
import {
  Sync as SyncIcon,
  Login as LoginIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Typography,
  Button,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  LinearProgress,
  Stack
} from '@mui/material';
import api from '../services/api';

interface DigiKeyStatus {
  api_configured: boolean;
  authenticated: boolean;
  sandbox_mode: boolean;
  sync_service_ready: boolean;
  message?: string;
  authorization_url?: string;
}

interface SyncResult {
  status: string;
  message: string;
  templates_synced?: number;
  templates_updated?: number;
  errors?: string[];
}

const DigiKeyAdmin: React.FC = () => {
  const [status, setStatus] = useState<DigiKeyStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authDialogOpen, setAuthDialogOpen] = useState(false);
  const [authCode, setAuthCode] = useState('');
  const [authUrl, setAuthUrl] = useState<string | null>(null);
  const [syncResults, setSyncResults] = useState<SyncResult[]>([]);
  const [syncInProgress, setSyncInProgress] = useState(false);
  const [selectedManufacturer, setSelectedManufacturer] = useState('Hager');

  const manufacturers = ['Hager', 'Schneider Electric', 'ABB', 'Eaton'];

  useEffect(() => {
    fetchStatus();
    fetchAuthUrl();
  }, []);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      const response = await api.get('/template-sync/status');
      setStatus(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch DigiKey status');
      console.error('Status fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAuthUrl = async () => {
    try {
      const response = await api.get('/template-sync/auth-url');
      if (response.data.authorization_url) {
        setAuthUrl(response.data.authorization_url);
      }
    } catch (err) {
      console.error('Failed to fetch auth URL:', err);
    }
  };

  const startOAuthFlow = () => {
    if (authUrl) {
      // Start the automated OAuth flow - user will be redirected to DigiKey and back
      window.location.href = authUrl;
    } else {
      setError('Authorization URL not available. Please check API configuration.');
    }
  };

  const authenticateWithCode = async () => {
    if (!authCode.trim()) return;

    try {
      setLoading(true);
      const response = await api.post('/template-sync/authenticate', {
        authorization_code: authCode.trim()
      });
      
      if (response.data.success) {
        setAuthDialogOpen(false);
        setAuthCode('');
        await fetchStatus();
        setError(null);
      } else {
        setError(response.data.message || 'Authentication failed');
      }
    } catch (err) {
      setError('Failed to authenticate with DigiKey');
      console.error('Authentication error:', err);
    } finally {
      setLoading(false);
    }
  };

  const initializePanelTemplates = async () => {
    try {
      setSyncInProgress(true);
      const response = await api.post('/template-sync/init-panels');
      setSyncResults(prev => [response.data, ...prev]);
    } catch (err) {
      setError('Failed to initialize panel templates');
      console.error('Panel init error:', err);
    } finally {
      setSyncInProgress(false);
    }
  };

  const syncManufacturer = async (manufacturer: string) => {
    try {
      setSyncInProgress(true);
      const response = await api.post(`/template-sync/sync/${manufacturer}`);
      setSyncResults(prev => [response.data, ...prev]);
    } catch (err) {
      setError(`Failed to sync ${manufacturer} components`);
      console.error('Sync error:', err);
    } finally {
      setSyncInProgress(false);
    }
  };

  const getStatusColor = () => {
    if (!status) return 'default';
    if (status.authenticated) return 'success';
    if (status.api_configured) return 'warning';
    return 'error';
  };

  const getStatusText = () => {
    if (!status) return 'Unknown';
    if (status.authenticated) return 'Authenticated';
    if (status.api_configured) return 'Ready for Auth';
    return 'Not Configured';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        DigiKey Integration Admin
      </Typography>

      {/* Status Card */}
      <Card sx={{ mb: 3 }}>
        <CardHeader
          title="DigiKey API Status"
          action={
            <Button
              startIcon={<RefreshIcon />}
              onClick={fetchStatus}
              disabled={loading}
            >
              Refresh
            </Button>
          }
        />
        <CardContent>
          {loading && !status ? (
            <CircularProgress />
          ) : status ? (
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Paper sx={{ p: 2, textAlign: 'center', minWidth: 150 }}>
                <Typography variant="subtitle2">Status</Typography>
                <Chip 
                  label={getStatusText()}
                  color={getStatusColor()}
                  sx={{ mt: 1 }}
                />
              </Paper>
              <Paper sx={{ p: 2, textAlign: 'center', minWidth: 150 }}>
                <Typography variant="subtitle2">API Configured</Typography>
                <Chip 
                  label={status.api_configured ? 'Yes' : 'No'}
                  color={status.api_configured ? 'success' : 'error'}
                  sx={{ mt: 1 }}
                />
              </Paper>
              <Paper sx={{ p: 2, textAlign: 'center', minWidth: 150 }}>
                <Typography variant="subtitle2">Authenticated</Typography>
                <Chip 
                  label={status.authenticated ? 'Yes' : 'No'}
                  color={status.authenticated ? 'success' : 'error'}
                  sx={{ mt: 1 }}
                />
              </Paper>
              <Paper sx={{ p: 2, textAlign: 'center', minWidth: 150 }}>
                <Typography variant="subtitle2">Mode</Typography>
                <Chip 
                  label={status.sandbox_mode ? 'Sandbox' : 'Production'}
                  color={status.sandbox_mode ? 'info' : 'warning'}
                  sx={{ mt: 1 }}
                />
              </Paper>
            </Stack>
          ) : null}

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Authentication Card */}
      <Card sx={{ mb: 3 }}>
        <CardHeader title="DigiKey Authentication" />
        <CardContent>
          {status?.authenticated ? (
            <Alert severity="success" icon={<CheckIcon />}>
              <Typography variant="body1">
                ✅ Successfully connected to DigiKey API
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                You can now sync component data from DigiKey.
              </Typography>
            </Alert>
          ) : (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                Connect to DigiKey to automatically sync electrical component data.
              </Typography>
              
              <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>What happens when you connect:</strong>
                </Typography>
                <Typography variant="body2" component="div">
                  • You'll be redirected to DigiKey for secure authorization
                  • After approval, you'll return here automatically
                  • Component templates will be available for synchronization
                </Typography>
              </Alert>
              
              <Button
                variant="contained"
                size="large"
                startIcon={<LoginIcon />}
                onClick={startOAuthFlow}
                disabled={!status?.api_configured || !authUrl || loading}
                sx={{ 
                  py: 1.5, 
                  px: 3,
                  fontSize: '1.1rem',
                  background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #1976D2 30%, #1AB7EA 90%)',
                  }
                }}
              >
                {loading ? 'Connecting...' : 'Connect to DigiKey'}
              </Button>
              
              {!status?.api_configured && (
                <Typography variant="caption" color="error" sx={{ display: 'block', mt: 1 }}>
                  API credentials not configured. Check environment variables.
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Sync Operations Card */}
      <Card sx={{ mb: 3 }}>
        <CardHeader title="Data Synchronization" />
        <CardContent>
          {syncInProgress && <LinearProgress sx={{ mb: 2 }} />}
          
          <Stack spacing={2}>
            <Button
              variant="outlined"
              onClick={initializePanelTemplates}
              disabled={syncInProgress}
            >
              Initialize Panel Templates
            </Button>
            
            <FormControl>
              <InputLabel>Manufacturer</InputLabel>
              <Select
                value={selectedManufacturer}
                onChange={(e) => setSelectedManufacturer(e.target.value)}
                disabled={syncInProgress}
              >
                {manufacturers.map((mfg) => (
                  <MenuItem key={mfg} value={mfg}>{mfg}</MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Button
              variant="contained"
              startIcon={<SyncIcon />}
              onClick={() => syncManufacturer(selectedManufacturer)}
              disabled={!status?.authenticated || syncInProgress}
            >
              Sync {selectedManufacturer} Components
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* Sync Results */}
      {syncResults.length > 0 && (
        <Card>
          <CardHeader title="Sync Results" />
          <CardContent>
            <List>
              {syncResults.map((result, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center">
                        {result.status === 'success' ? (
                          <CheckIcon color="success" sx={{ mr: 1 }} />
                        ) : (
                          <ErrorIcon color="error" sx={{ mr: 1 }} />
                        )}
                        {result.message}
                      </Box>
                    }
                    secondary={
                      result.templates_synced !== undefined && (
                        `${result.templates_synced} templates synced, ${result.templates_updated} updated`
                      )
                    }
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

      {/* Authentication Dialog */}
      <Dialog open={authDialogOpen} onClose={() => setAuthDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {authCode ? 'Complete Authentication' : 'Enter Authorization Code'}
        </DialogTitle>
        <DialogContent>
          {authCode ? (
            <Alert severity="success" sx={{ mb: 2 }}>
              Authorization code received automatically! Click "Authenticate" to complete the process.
            </Alert>
          ) : (
            <Alert severity="info" sx={{ mb: 2 }}>
              After authorizing with DigiKey, you'll be redirected back here automatically.
              If the code wasn't captured automatically, you can paste it below.
            </Alert>
          )}
          <TextField
            autoFocus={!authCode}
            margin="dense"
            label="Authorization Code"
            fullWidth
            value={authCode}
            onChange={(e) => setAuthCode(e.target.value)}
            placeholder="e.g., ABC123XYZ"
            helperText={authCode ? "Code detected from callback" : "Enter authorization code manually if needed"}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setAuthDialogOpen(false);
            setAuthCode('');
          }}>
            Cancel
          </Button>
          <Button
            onClick={authenticateWithCode}
            disabled={!authCode.trim() || loading}
            variant="contained"
          >
            {loading ? <CircularProgress size={20} /> : 'Authenticate'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DigiKeyAdmin;