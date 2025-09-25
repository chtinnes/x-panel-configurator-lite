import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  TextField,
  InputAdornment,
  Collapse,
  ListItem,
  ListItemButton,
  ListItemText,
  IconButton,
} from '@mui/material';
import { 
  Search as SearchIcon, 
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon 
} from '@mui/icons-material';
import { useDrag, DragSourceMonitor } from 'react-dnd';
import { DeviceTemplate } from '../types';
import { templateAPI } from '../services/api';

interface DeviceItemProps {
  device: DeviceTemplate;
}

const DeviceItem: React.FC<DeviceItemProps> = ({ device }) => {
  const [{ isDragging }, drag] = useDrag({
    type: 'device',
    item: device,
    collect: (monitor: DragSourceMonitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  return (
    <Card
      ref={drag}
      className={`device-item ${isDragging ? 'dragging' : ''}`}
      sx={{
        mb: 1,
        cursor: 'move',
        opacity: isDragging ? 0.5 : 1,
        '&:hover': {
          backgroundColor: '#f0f0f0',
        },
      }}
    >
      <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
        <Typography variant="subtitle2" component="div">
          {device.name}
        </Typography>
        <Typography variant="caption" color="text.secondary" display="block">
          {device.model} - {device.manufacturer}
        </Typography>
        <Box sx={{ display: 'flex', gap: 0.5, mt: 1, flexWrap: 'wrap' }}>
          {device.max_current && (
            <Chip label={`${device.max_current}A`} size="small" />
          )}
          {device.slots_required > 1 && (
            <Chip label={`${device.slots_required} slots`} size="small" color="warning" />
          )}
          <Chip label={device.category} size="small" color="primary" />
        </Box>
        {device.description && (
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            {device.description}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

const DeviceLibrary: React.FC = () => {
  const [devices, setDevices] = useState<DeviceTemplate[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    Protection: true,
    Measurement: false,
    Control: false,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      setLoading(true);
      const response = await templateAPI.getDeviceLibrary();
      setDevices(response.data);
    } catch (err) {
      console.error('Error fetching device library:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredDevices = devices.filter(device =>
    device.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const devicesByCategory = filteredDevices.reduce((acc, device) => {
    if (!acc[device.category]) {
      acc[device.category] = [];
    }
    acc[device.category].push(device);
    return acc;
  }, {} as Record<string, DeviceTemplate[]>);

  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category],
    }));
  };

  if (loading) {
    return <Typography variant="body2">Loading devices...</Typography>;
  }

  return (
    <Box>
      <TextField
        size="small"
        placeholder="Search devices..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        fullWidth
        sx={{ mb: 2 }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />

      {Object.entries(devicesByCategory).map(([category, categoryDevices]) => (
        <Box key={category} sx={{ mb: 2 }}>
          <ListItem disablePadding sx={{ px: 0 }}>
            <ListItemButton onClick={() => toggleCategory(category)}>
              <ListItemText
                primary={
                  <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                    {category} ({categoryDevices.length})
                  </Typography>
                }
              />
              <IconButton size="small">
                {expandedCategories[category] ? <ExpandLessIcon /> : <ExpandMoreIcon />}
              </IconButton>
            </ListItemButton>
          </ListItem>
          
          <Collapse in={expandedCategories[category]}>
            <Box>
              {categoryDevices.map((device, index) => (
                <DeviceItem key={`${category}-${index}`} device={device} />
              ))}
            </Box>
          </Collapse>
        </Box>
      ))}

      {filteredDevices.length === 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mt: 2 }}>
          No devices found matching your search.
        </Typography>
      )}

      <Box sx={{ mt: 2, p: 1, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
        <Typography variant="caption" color="text.secondary">
          💡 Drag devices from here to panel slots to configure your installation.
        </Typography>
      </Box>
    </Box>
  );
};

export default DeviceLibrary;
