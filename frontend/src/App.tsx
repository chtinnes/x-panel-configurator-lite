import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Card,
  CardContent,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
} from '@mui/material';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import PanelView from './components/PanelView';
import DeviceLibrary from './components/DeviceLibrary';
import WiringView from './components/WiringView';
import PanelSelector from './components/PanelSelector';
import DigiKeyAdmin from './components/DigiKeyAdmin';
import DigiKeyOAuthCallback from './components/DigiKeyOAuthCallback';
import SSLCertificateHelper from './components/SSLCertificateHelper';
import { Panel } from './types';
import './App.css';

function AppContent() {
  const [selectedPanel, setSelectedPanel] = useState<Panel | null>(null);
  const [currentView, setCurrentView] = useState<'panel' | 'wiring' | 'admin'>('panel');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Check if we're on the admin route and switch view accordingly
    if (location.pathname === '/admin') {
      setCurrentView('admin');
    }
  }, [location]);

  const handlePanelSelect = (panel: Panel) => {
    setSelectedPanel(panel);
  };

  const handlePanelUpdate = (updatedPanel: Panel) => {
    setSelectedPanel(updatedPanel);
  };

  const handleViewChange = (view: 'panel' | 'wiring' | 'admin') => {
    setCurrentView(view);
    if (view === 'admin') {
      navigate('/admin');
    } else {
      navigate('/');
    }
  };

  return (
    <SSLCertificateHelper>
      <DndProvider backend={HTML5Backend}>
        <Box sx={{ display: 'flex' }}>
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <Typography variant="h6" noWrap component="div">
                Electrical Panel Configurator
              </Typography>
            </Toolbar>
          </AppBar>
        
        <Drawer
          variant="permanent"
          sx={{
            width: 300,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: { width: 300, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <Box sx={{ overflow: 'auto', p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Panel Selection
            </Typography>
            <PanelSelector onPanelSelect={handlePanelSelect} />
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="h6" gutterBottom>
              Navigation
            </Typography>
            <List>
              <ListItem disablePadding>
                <ListItemButton
                  selected={currentView === 'panel'}
                  onClick={() => handleViewChange('panel')}
                >
                  <ListItemText primary="Panel Configuration" />
                </ListItemButton>
              </ListItem>
              <ListItem disablePadding>
                <ListItemButton
                  selected={currentView === 'wiring'}
                  onClick={() => handleViewChange('wiring')}
                >
                  <ListItemText primary="Wiring Configuration" />
                </ListItemButton>
              </ListItem>
              <ListItem disablePadding>
                <ListItemButton
                  selected={currentView === 'admin'}
                  onClick={() => handleViewChange('admin')}
                >
                  <ListItemText primary="DigiKey Admin" />
                </ListItemButton>
              </ListItem>
            </List>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="h6" gutterBottom>
              Device Library
            </Typography>
            <DeviceLibrary />
          </Box>
        </Drawer>

        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <Toolbar />
          {currentView === 'admin' ? (
            <>
              <Typography variant="h4" gutterBottom>
                DigiKey Administration
              </Typography>
              <DigiKeyAdmin />
            </>
          ) : selectedPanel ? (
            <>
              <Typography variant="h4" gutterBottom>
                {selectedPanel.name}
              </Typography>
              <Typography variant="subtitle1" gutterBottom color="text.secondary">
                {selectedPanel.template ? 
                  `${selectedPanel.template.manufacturer} ${selectedPanel.template.model} - ${selectedPanel.template.total_slots} slots (${selectedPanel.template.rows} rows × ${selectedPanel.template.slots_per_row} slots), ${selectedPanel.template.voltage}V, ${selectedPanel.template.max_current}A` :
                  'Panel template information not available'
                }
              </Typography>
              
              {currentView === 'panel' && <PanelView panel={selectedPanel} onPanelUpdate={handlePanelUpdate} />}
              {currentView === 'wiring' && <WiringView panel={selectedPanel} />}
            </>
          ) : (
            <Card>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Welcome to Electrical Panel Configurator
                </Typography>
                <Typography variant="body1">
                  Select or create a panel from the sidebar to begin configuring your electrical installation.
                </Typography>
                <Typography variant="body2" sx={{ mt: 2 }}>
                  Features:
                </Typography>
                <List dense>
                  <ListItem>• Configure panel slots with circuit breakers, RCDs, and other devices</ListItem>
                  <ListItem>• Manage wiring connections between devices</ListItem>
                  <ListItem>• Use pre-configured Hager Volta panel templates</ListItem>
                  <ListItem>• Access a comprehensive device library</ListItem>
                </List>
              </CardContent>
            </Card>
          )}
        </Box>
      </Box>
    </DndProvider>
    </SSLCertificateHelper>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/template-sync/callback" element={<DigiKeyOAuthCallback />} />
        <Route path="/admin" element={<AppContent />} />
        <Route path="/" element={<AppContent />} />
      </Routes>
    </Router>
  );
}

export default App;
