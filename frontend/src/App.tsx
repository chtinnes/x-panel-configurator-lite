import React, { useState } from 'react';
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
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import PanelView from './components/PanelView';
import DeviceLibrary from './components/DeviceLibrary';
import WiringView from './components/WiringView';
import PanelSelector from './components/PanelSelector';
import { Panel } from './types';
import './App.css';

function App() {
  const [selectedPanel, setSelectedPanel] = useState<Panel | null>(null);
  const [currentView, setCurrentView] = useState<'panel' | 'wiring'>('panel');

  const handlePanelSelect = (panel: Panel) => {
    setSelectedPanel(panel);
  };

  const handleViewChange = (view: 'panel' | 'wiring') => {
    setCurrentView(view);
  };

  return (
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
          {selectedPanel ? (
            <>
              <Typography variant="h4" gutterBottom>
                {selectedPanel.name}
              </Typography>
              <Typography variant="subtitle1" gutterBottom color="text.secondary">
                {selectedPanel.manufacturer} {selectedPanel.model} - {selectedPanel.total_slots} slots ({selectedPanel.rows} rows × {selectedPanel.slots_per_row} slots), {selectedPanel.voltage}V, {selectedPanel.current_rating}A
              </Typography>
              
              {currentView === 'panel' && <PanelView panel={selectedPanel} />}
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
  );
}

export default App;
