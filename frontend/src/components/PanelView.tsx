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
import { Panel, PanelSlot, DeviceType, DeviceLibraryItem } from '../types';
import { deviceAPI, panelAPI } from '../services/api';

interface PanelViewProps {
  panel: Panel;
  onPanelUpdate?: (panel: Panel) => void;
}

interface SlotProps {
  slot: PanelSlot;
  onSlotUpdate: (slotNumber: number, deviceId: number | null, label?: string, currentSetting?: number, slotsRequired?: number) => void;
}

const SlotComponent: React.FC<SlotProps> = ({ slot, onSlotUpdate }) => {
  const [{ isOver, canDrop }, drop] = useDrop({
    accept: 'device',
    drop: async (item: DeviceLibraryItem) => {
      // For now, use library device ID directly for validation
      // In a real app, you'd map library devices to DeviceType IDs
      onSlotUpdate(slot.slot_number, item.id, undefined, undefined, item.slots_required);
    },
    canDrop: (item: DeviceLibraryItem) => {
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

  const isEmpty = !slot.device_type_id && !slot.is_occupied;
  const isBlocked = slot.is_occupied && !slot.device_type_id; // Blocked by multi-slot device
  const hasDevice = slot.device_type_id && slot.is_occupied;
  
  return (
    <Card
      ref={drop}
      sx={{
        minHeight: 120,
        backgroundColor: isEmpty 
          ? (isOver && canDrop ? '#e3f2fd' : '#f5f5f5') 
          : isBlocked
          ? '#ffebee' // Light red for blocked slots
          : '#ffffff', // White for occupied slots
        border: isEmpty 
          ? (isOver && canDrop ? '2px dashed #2196f3' : '2px dashed #cccccc')
          : isBlocked
          ? '2px solid #f44336' // Red border for blocked
          : hasDevice
          ? '2px solid #4caf50' // Green border for devices
          : '2px solid #cccccc',
        cursor: isEmpty ? 'pointer' : 'default',
        transition: 'all 0.2s ease',
        '&:hover': {
          backgroundColor: isEmpty ? '#eeeeee' : isBlocked ? '#ffebee' : '#ffffff',
        },
        opacity: isBlocked ? 0.7 : 1, // Make blocked slots more transparent
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
        ) : hasDevice && slot.device_type ? (
          <Box sx={{ mt: 1 }}>
            <Typography variant="subtitle2" component="div">
              {slot.device_label || 'Unnamed Device'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {slot.device_type.name}
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
  const [devices, setDevices] = useState<DeviceType[]>([]);
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
        const totalSlots = panel.rows * panel.slots_per_row;
        
        for (let row = 1; row <= panel.rows; row++) {
          for (let col = 1; col <= panel.slots_per_row; col++) {
            if (slotNumber <= totalSlots) {
              initialSlots.push({
                id: slotNumber,
                panel_id: panel.id,
                slot_number: slotNumber,
                row: row,
                column: col,
                device_type_id: undefined,
                device_label: undefined,
                current_setting: undefined,
                is_occupied: false,
                spans_slots: 1,
                device_type: undefined,
              });
              slotNumber++;
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
  }, [panel.id, panel.rows, panel.slots_per_row, onPanelUpdate]);

  useEffect(() => {
    fetchPanelData();
    fetchDevices();
  }, [panel.id, panel.rows, panel.slots_per_row, fetchPanelData]);

  const fetchDevices = async () => {
    try {
      const response = await deviceAPI.getHagerDeviceLibrary();
      setDevices(response.data);
    } catch (err) {
      console.error('Error fetching devices:', err);
    }
  };

  const handleSlotUpdate = async (slotNumber: number, deviceId: number | null, label?: string, currentSetting?: number, slotsRequired?: number) => {
    try {
      const slot = slots.find(s => s.slot_number === slotNumber);
      if (!slot) {
        setError('Slot not found');
        return;
      }

      if (!deviceId) {
        // Remove device using API
        await deviceAPI.removeDeviceFromSlot(slot.id);
        
        // Refresh panel data to get updated state
        await fetchPanelData();
      } else {
        // For device placement, we need to handle the library-to-database mapping
        let actualDeviceTypeId = deviceId;
        
        // Check if this is a library device that needs to be created in the database
        const existingDeviceTypes = await deviceAPI.getAllDeviceTypes();
        const existingDevice = existingDeviceTypes.data.find((dt: any) => dt.id === deviceId);
        
        if (!existingDevice) {
          // This is a library device - need to create it in the database first
          const libraryDevices = await deviceAPI.getHagerDeviceLibrary();
          const libraryDevice = libraryDevices.data.find((ld: any) => ld.id === deviceId);
          
          if (libraryDevice) {
            const createdDevice = await deviceAPI.createDeviceType({
              name: libraryDevice.name,
              category: libraryDevice.category,
              manufacturer: libraryDevice.manufacturer,
              model: libraryDevice.model,
              slots_required: libraryDevice.slots_required,
              max_current: libraryDevice.max_current,
              voltage_range: libraryDevice.voltage_range,
              description: libraryDevice.description,
            });
            actualDeviceTypeId = createdDevice.data.id;
          } else {
            setError('Device not found in library');
            return;
          }
        }

        // Place device using API
        await deviceAPI.updatePanelSlot(slot.id, {
          device_type_id: actualDeviceTypeId,
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
    }
  };

  const handleSlotClick = (slot: PanelSlot) => {
    if (slot.device_type_id) {
      setConfigDialog({ open: true, slot });
      setSelectedDeviceId(slot.device_type_id);
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
    
    for (let row = 1; row <= panel.rows; row++) {
      const rowSlots = slots
        .filter(slot => slot.row === row)
        .sort((a, b) => a.column - b.column);
      rowsArray.push(rowSlots);
    }
    
    return rowsArray;
  };

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Panel Configuration
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label={`${panel.total_slots} slots`}
            variant="outlined"
          />
          <Chip
            label={`${panel.rows} rows × ${panel.slots_per_row} slots`}
            variant="outlined"
            color="primary"
          />
          <Chip
            label={`${panel.voltage}V`}
            variant="outlined"
          />
          <Chip
            label={`${panel.current_rating}A`}
            variant="outlined"
          />
        </Box>
      </Box>

      {/* Panel Layout by Rows */}
      <Box sx={{ border: '2px solid #ddd', borderRadius: 2, p: 2, backgroundColor: '#f9f9f9' }}>
        {organizeSlotsByRows().map((rowSlots, rowIndex) => (
          <Box key={rowIndex} sx={{ mb: rowIndex < panel.rows - 1 ? 2 : 0 }}>
            <Typography variant="subtitle2" color="text.secondary" sx={{ mb: 1 }}>
              Row {rowIndex + 1}
            </Typography>
            <Grid container spacing={1}>
              {rowSlots.map((slot) => (
                <Grid 
                  key={slot.slot_number}
                  size={{ xs: 12 / panel.slots_per_row }}
                >
                  <Box onClick={() => handleSlotClick(slot)}>
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
            <TextField
              select
              label="Device Type"
              value={selectedDeviceId || ''}
              onChange={(e) => setSelectedDeviceId(Number(e.target.value))}
              fullWidth
            >
              <MenuItem value="">None</MenuItem>
              {devices.map((device) => (
                <MenuItem key={device.id} value={device.id}>
                  {device.name} - {device.model}
                </MenuItem>
              ))}
            </TextField>

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