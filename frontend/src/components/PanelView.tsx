import React, { useState, useEffect } from 'react';
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
import { deviceAPI } from '../services/api';

interface PanelViewProps {
  panel: Panel;
}

interface SlotProps {
  slot: PanelSlot;
  onSlotUpdate: (slotNumber: number, deviceId: number | null, label?: string, currentSetting?: number) => void;
}

const SlotComponent: React.FC<SlotProps> = ({ slot, onSlotUpdate }) => {
  const [{ isOver }, drop] = useDrop({
    accept: 'device',
    drop: (item: DeviceLibraryItem) => {
      onSlotUpdate(slot.slot_number, item.id);
    },
    collect: (monitor: DropTargetMonitor) => ({
      isOver: monitor.isOver(),
    }),
  });

  const isEmpty = !slot.device_type_id;
  
  return (
    <Card
      ref={drop}
      sx={{
        minHeight: 120,
        backgroundColor: isEmpty 
          ? (isOver ? '#e3f2fd' : '#f5f5f5') 
          : '#ffffff',
        border: isEmpty 
          ? (isOver ? '2px dashed #2196f3' : '2px dashed #cccccc')
          : '2px solid #4caf50',
        cursor: isEmpty ? 'pointer' : 'default',
        transition: 'all 0.2s ease',
        '&:hover': {
          backgroundColor: isEmpty ? '#eeeeee' : '#ffffff',
        },
      }}
    >
      <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
        <Typography variant="caption" color="text.secondary">
          Slot {slot.slot_number}
        </Typography>
        
        {isEmpty ? (
          <Box sx={{ textAlign: 'center', mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {isOver ? 'Drop device here' : 'Empty slot'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Drag device from library
            </Typography>
          </Box>
        ) : (
          <Box sx={{ mt: 1 }}>
            <Typography variant="subtitle2" component="div">
              {slot.device_label || 'Unnamed Device'}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Device ID: {slot.device_type_id}
            </Typography>
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
        )}
      </CardContent>
    </Card>
  );
};

const PanelView: React.FC<PanelViewProps> = ({ panel }) => {
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

  useEffect(() => {
    // Initialize slots from panel configuration organized by rows
    const initialSlots: PanelSlot[] = [];
    let slotNumber = 1;
    
    for (let row = 1; row <= panel.rows; row++) {
      for (let col = 1; col <= panel.slots_per_row; col++) {
        if (slotNumber <= panel.total_slots) {
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
          });
          slotNumber++;
        }
      }
    }
    
    setSlots(initialSlots);
    fetchDevices();
  }, [panel.id, panel.total_slots, panel.rows, panel.slots_per_row]);

  const fetchDevices = async () => {
    try {
      const response = await deviceAPI.getHagerDeviceLibrary();
      setDevices(response.data);
    } catch (err) {
      console.error('Error fetching devices:', err);
    }
  };

  const handleSlotUpdate = (slotNumber: number, deviceId: number | null, label?: string, currentSetting?: number) => {
    // Update local state (simulating API call since backend methods don't exist yet)
    setSlots(prev => prev.map(slot => 
      slot.slot_number === slotNumber ? {
        ...slot,
        device_type_id: deviceId,
        device_label: label,
        current_setting: currentSetting,
        is_occupied: !!deviceId,
      } : slot
    ));
    
    setError(null);
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
      handleSlotUpdate(
        configDialog.slot.slot_number,
        selectedDeviceId,
        deviceLabel,
        currentRating
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