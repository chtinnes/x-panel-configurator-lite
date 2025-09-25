import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Chip,
  Alert,
} from '@mui/material';
import { useDrop, DropTargetMonitor } from 'react-dnd';
import { Panel, PanelSlot, DeviceTemplate } from '../types';
import { deviceAPI, panelAPI } from '../services/api';

interface PanelViewProps {
  panel: Panel;
  onPanelUpdate?: (panel: Panel) => void;
}

interface SlotProps {
  slot: PanelSlot;
  onSlotUpdate: (slotNumber: number, deviceTemplateId: number | null, label?: string, currentSetting?: number, slotsRequired?: number) => void;
}

const SlotComponent: React.FC<SlotProps> = ({ slot, onSlotUpdate }) => {
  const [{ isOver, canDrop }, drop] = useDrop({
    accept: 'device',
    drop: async (item: DeviceTemplate) => {
      // Use device template ID directly
      onSlotUpdate(slot.slot_number, item.id, undefined, undefined, item.slots_required);
    },
    canDrop: (item: DeviceTemplate) => {
      // Basic validation: single slot devices can be placed anywhere that's not occupied
      // Multi-slot devices need more complex validation
      if (slot.is_occupied) {
        return false;
      }
      
      // For multi-slot devices, we'll do the validation in the drop handler
      return true;
    },
    collect: (monitor: DropTargetMonitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  });

  const isEmpty = !slot.device_template_id && !slot.is_occupied;
  const isBlocked = slot.is_occupied && !slot.device_template_id; // Blocked by multi-slot device
  const hasDevice = slot.device_template_id && slot.is_occupied;
  
  return (
    <Card
      ref={drop}
      sx={{
        minHeight: 120,
        backgroundColor: isEmpty 
          ? (isOver && canDrop ? 'rgba(227, 242, 253, 0.8)' : 'rgba(245, 245, 245, 0.6)') 
          : isBlocked
          ? 'rgba(255, 235, 238, 0.8)' // Light red for blocked slots with transparency
          : 'rgba(255, 255, 255, 0.85)', // Semi-transparent white for occupied slots
        border: isEmpty 
          ? (isOver && canDrop ? '2px dashed #2196f3' : '2px dashed #cccccc')
          : isBlocked
          ? '2px solid #f44336' // Red border for blocked
          : hasDevice
          ? '2px solid #4caf50' // Green border for devices
          : '2px solid #cccccc',
        cursor: isEmpty ? 'pointer' : 'default',
        transition: 'all 0.2s ease',
        borderRadius: hasDevice ? '4px' : '6px',
        boxShadow: hasDevice 
          ? '0 2px 8px rgba(0,0,0,0.15), inset 0 1px 2px rgba(255,255,255,0.5)' 
          : '0 1px 3px rgba(0,0,0,0.1)',
        '&:hover': {
          backgroundColor: isEmpty 
            ? 'rgba(238, 238, 238, 0.7)' 
            : isBlocked 
            ? 'rgba(255, 235, 238, 0.9)' 
            : 'rgba(255, 255, 255, 0.95)',
          transform: hasDevice ? 'translateY(-1px)' : 'none',
          boxShadow: hasDevice 
            ? '0 4px 12px rgba(0,0,0,0.2), inset 0 1px 2px rgba(255,255,255,0.5)' 
            : '0 2px 4px rgba(0,0,0,0.15)',
        },
        opacity: isBlocked ? 0.7 : 1,
        // Add device mounting appearance with transparency
        background: hasDevice 
          ? 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,248,248,0.8) 50%, rgba(240,240,240,0.7) 100%)'
          : undefined,
        // Add mounting rail connection visual
        position: 'relative',
        '&::before': hasDevice ? {
          content: '""',
          position: 'absolute',
          bottom: '-2px',
          left: '10%',
          right: '10%',
          height: '4px',
          backgroundColor: '#666',
          borderRadius: '0 0 2px 2px',
          boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.3)',
        } : {},
      }}
    >
      <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
        <Typography variant="caption" color="text.secondary">
          Slot {slot.slot_number}
        </Typography>
        
        {isEmpty ? (
          <Box sx={{ textAlign: 'center', mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {isOver && canDrop ? 'Drop device here' : 
               isOver && !canDrop ? 'Cannot place here' : 'Empty slot'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Drag device from library
            </Typography>
          </Box>
        ) : isBlocked ? (
          <Box sx={{ textAlign: 'center', mt: 1 }}>
            <Typography variant="body2" color="error" sx={{ fontWeight: 'bold' }}>
              BLOCKED
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Used by multi-slot device
            </Typography>
          </Box>
        ) : hasDevice && slot.device_template ? (
          <Box sx={{ mt: 1, position: 'relative' }}>
            {/* Device Switch/Toggle Visual */}
            <Box sx={{ 
              position: 'absolute',
              top: -5,
              right: 5,
              width: 20,
              height: 12,
              backgroundColor: '#4caf50',
              borderRadius: '6px',
              border: '1px solid #388e3c',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              '&::after': {
                content: '""',
                width: 8,
                height: 8,
                backgroundColor: '#ffffff',
                borderRadius: '50%',
                boxShadow: '0 1px 2px rgba(0,0,0,0.3)',
              }
            }} />
            
            {/* LED Indicator - only show when device is active/configured */}
            {slot.current_setting && (
              <Box sx={{
                position: 'absolute',
                top: -5,
                right: 30,
                width: 6,
                height: 6,
                backgroundColor: '#4caf50',
                borderRadius: '50%',
                boxShadow: '0 0 4px #4caf50, 0 0 8px rgba(76, 175, 80, 0.5)',
              }} />
            )}
            
            <Typography variant="subtitle2" component="div" sx={{ fontWeight: 'bold', fontSize: '0.8rem' }}>
              {slot.device_label || 'Unnamed Device'}
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
              {slot.device_template.name}
            </Typography>
            {slot.spans_slots > 1 && (
              <Chip
                label={`Spans ${slot.spans_slots} slots`}
                size="small"
                color="info"
                sx={{ mt: 0.5, mr: 0.5 }}
              />
            )}
            {slot.current_setting && (
              <Box sx={{ mt: 1 }}>
                <Chip
                  label={`${slot.current_setting}A`}
                  size="small"
                  color="primary"
                />
              </Box>
            )}
            <Button
              size="small"
              variant="outlined"
              color="error"
              sx={{ mt: 1 }}
              onClick={(e) => {
                e.stopPropagation();
                onSlotUpdate(slot.slot_number, null);
              }}
            >
              Remove
            </Button>
          </Box>
        ) : null}
      </CardContent>
    </Card>
  );
};

const PanelView: React.FC<PanelViewProps> = ({ panel, onPanelUpdate }) => {
  const [slots, setSlots] = useState<PanelSlot[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [configDialog, setConfigDialog] = useState<{
    open: boolean;
    slot: PanelSlot | null;
  }>({
    open: false,
    slot: null,
  });
  const [selectedDeviceId, setSelectedDeviceId] = useState<number | null>(null);
  const [deviceLabel, setDeviceLabel] = useState('');
  const [currentSetting, setCurrentSetting] = useState('');

  const fetchPanelData = useCallback(async () => {
    try {
      // Fetch the panel with its slots from the backend
      const panelResponse = await panelAPI.getPanel(panel.id);
      const panelWithSlots = panelResponse.data;
      
      if (panelWithSlots.slots && panelWithSlots.slots.length > 0) {
        // Use the actual slots from the backend
        setSlots(panelWithSlots.slots);
      } else {
        // Panel exists but has no slots yet - initialize them
        const initialSlots: PanelSlot[] = [];
        let slotNumber = 1;
        const totalSlots = panel.template ? panel.template.rows * panel.template.slots_per_row : 0;
        
        if (panel.template) {
          for (let row = 1; row <= panel.template.rows; row++) {
            for (let col = 1; col <= panel.template.slots_per_row; col++) {
              if (slotNumber <= totalSlots) {
                initialSlots.push({
                  id: slotNumber,
                  panel_id: panel.id,
                  slot_number: slotNumber,
                  row: row,
                  column: col,
                  device_template_id: undefined,
                  device_label: undefined,
                  current_setting: undefined,
                  is_occupied: false,
                  spans_slots: 1,
                  device_template: undefined,
                });
                slotNumber++;
              }
            }
          }
        }
        setSlots(initialSlots);
      }
      
      // If callback provided, update the parent component with the fresh panel data
      if (onPanelUpdate) {
        onPanelUpdate(panelWithSlots);
      }
    } catch (err) {
      console.error('Error fetching panel data:', err);
      setError('Failed to load panel configuration');
    }
  }, [panel.id, panel.template?.rows, panel.template?.slots_per_row, onPanelUpdate]);

  useEffect(() => {
    fetchPanelData();
    fetchDevices();
  }, [panel.id, panel.template?.rows, panel.template?.slots_per_row, fetchPanelData]);

  const fetchDevices = async () => {
    // No longer needed - templates are fetched directly from the library
  };

  const handleSlotUpdate = async (slotNumber: number, deviceTemplateId: number | null, label?: string, currentSetting?: number, slotsRequired?: number) => {
    // Clear any existing errors when starting a new operation
    setError(null);
    
    try {
      const slot = slots.find(s => s.slot_number === slotNumber);
      if (!slot) {
        setError('Slot not found');
        return;
      }

      if (!deviceTemplateId) {
        // Remove device using API
        await deviceAPI.updatePanelSlot(slot.id, {
          device_template_id: null,
          device_label: undefined,
          current_setting: undefined,
        });
        
        // Refresh panel data to get updated state
        await fetchPanelData();
      } else {
        // Place device using template ID directly
        await deviceAPI.updatePanelSlot(slot.id, {
          device_template_id: deviceTemplateId,
          device_label: label,
          current_setting: currentSetting,
        });
        
        // Refresh panel data to get updated state
        await fetchPanelData();
      }
      
      setError(null);
    } catch (err: any) {
      console.error('Error updating slot:', err);
      setError(err.response?.data?.detail || 'Failed to update slot configuration');
      
      // Always refresh panel data to ensure UI consistency, even after errors
      try {
        await fetchPanelData();
      } catch (refreshErr) {
        console.error('Error refreshing panel data after failed operation:', refreshErr);
      }
    }
  };

  const handleSlotClick = (slot: PanelSlot) => {
    if (slot.device_template_id) {
      setConfigDialog({ open: true, slot });
      setSelectedDeviceId(slot.device_template_id);
      setDeviceLabel(slot.device_label || '');
      setCurrentSetting(slot.current_setting?.toString() || '');
    }
  };

  const handleConfigSave = () => {
    if (configDialog.slot) {
      const currentRating = currentSetting ? parseInt(currentSetting) : undefined;
      // For configuration updates, we don't change the device placement, just settings
      handleSlotUpdate(
        configDialog.slot.slot_number,
        selectedDeviceId,
        deviceLabel,
        currentRating,
        undefined // Don't change slot blocking for config updates
      );
    }
    setConfigDialog({ open: false, slot: null });
  };

  const handleConfigCancel = () => {
    setConfigDialog({ open: false, slot: null });
    setSelectedDeviceId(null);
    setDeviceLabel('');
    setCurrentSetting('');
  };

  // Group slots by rows for display
  const organizeSlotsByRows = () => {
    const rowsArray: PanelSlot[][] = [];
    const rows = panel.template ? panel.template.rows : 0;
    
    for (let row = 1; row <= rows; row++) {
      const rowSlots = slots
        .filter(slot => slot.row === row)
        .sort((a, b) => a.column - b.column);
      rowsArray.push(rowSlots);
    }
    
    return rowsArray;
  };

  const handleErrorDismiss = () => {
    setError(null);
  };

  // Auto-dismiss errors after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [error]);

  return (
    <Box>
      {/* Dismissible Error Alert */}
      {error && (
        <Alert 
          severity="error" 
          onClose={handleErrorDismiss}
          sx={{ mb: 2 }}
        >
          {error}
        </Alert>
      )}
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Panel Configuration
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label={`${panel.template?.total_slots || 0} slots`}
            variant="outlined"
          />
          <Chip
            label={`${panel.template?.rows || 0} rows × ${panel.template?.slots_per_row || 0} slots`}
            variant="outlined"
            color="primary"
          />
          <Chip
            label={`${panel.template?.voltage || 0}V`}
            variant="outlined"
          />
          <Chip
            label={`${panel.template?.max_current || 0}A`}
            variant="outlined"
          />
        </Box>
      </Box>

      {/* Panel Layout by Rows */}
      <Box className="panel-enclosure">
        {organizeSlotsByRows().map((rowSlots, rowIndex) => (
          <Box key={rowIndex} className="panel-row">
            {/* DIN Rail Background */}
            <Box className="din-rail">
              <Box className="din-rail-screws">
                <Box className="din-rail-screw"></Box>
                <Box className="din-rail-screw"></Box>
              </Box>
            </Box>
            
            {/* Row Label */}
            <Typography 
              variant="subtitle2" 
              color="text.secondary" 
              sx={{ 
                mb: 1, 
                position: 'relative', 
                zIndex: 3,
                backgroundColor: 'rgba(255,255,255,0.8)',
                padding: '2px 8px',
                borderRadius: '4px',
                display: 'inline-block',
                fontSize: '0.75rem',
                fontWeight: 'bold'
              }}
            >
              Row {rowIndex + 1}
            </Typography>
            
            {/* Device Slots */}
            <Grid container spacing={1} sx={{ position: 'relative', zIndex: 2 }}>
              {rowSlots.map((slot) => (
                <Grid 
                  key={slot.slot_number}
                  size={{ xs: 12 / (panel.template?.slots_per_row || 1) }}
                >
                  <Box 
                    onClick={() => handleSlotClick(slot)}
                    className="device-slot"
                  >
                    <SlotComponent
                      slot={slot}
                      onSlotUpdate={handleSlotUpdate}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Box>
        ))}
      </Box>

      {/* Configuration Dialog */}
      <Dialog open={configDialog.open} onClose={handleConfigCancel} maxWidth="sm" fullWidth>
        <DialogTitle>
          Configure Slot {configDialog.slot?.slot_number}
        </DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {configDialog.slot?.device_template && (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Device: {configDialog.slot.device_template.name} - {configDialog.slot.device_template.model}
              </Typography>
            )}
            
            <TextField
              label="Device Label"
              value={deviceLabel}
              onChange={(e) => setDeviceLabel(e.target.value)}
              placeholder="Enter a custom label for this device"
              fullWidth
            />

            <TextField
              label="Current Rating (A)"
              value={currentSetting}
              onChange={(e) => setCurrentSetting(e.target.value)}
              placeholder="Enter current rating in amperes"
              type="number"
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleConfigCancel}>Cancel</Button>
          <Button onClick={handleConfigSave} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Box sx={{ mt: 3, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
        <Typography variant="body2" color="text.secondary">
          💡 <strong>Instructions:</strong><br />
          • Drag devices from the library on the left to empty slots<br />
          • Click on filled slots to configure device settings<br />
          • Use the wiring view to connect devices together<br />
          • RCBOs require 2 adjacent slots, Smart meters require 4 slots
        </Typography>
      </Box>
    </Box>
  );
};

export default PanelView;