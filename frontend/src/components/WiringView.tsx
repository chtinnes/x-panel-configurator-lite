import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Alert,
  Grid,
} from '@mui/material';
import { 
  Add as AddIcon, 
  Edit as EditIcon, 
  Delete as DeleteIcon,
  Cable as CableIcon 
} from '@mui/icons-material';
import { Panel, Wire, WireCreate, PanelSlot } from '../types';
import { wiringAPI, panelAPI } from '../services/api';

interface WiringViewProps {
  panel: Panel;
}

interface WireFormData {
  label: string;
  wire_type: string;
  cross_section: number;
  color: string;
  source_slot_id: number | '';
  destination_slot_id: number | '';
  external_source: string;
  external_destination: string;
  length: number | '';
}

const WiringView: React.FC<WiringViewProps> = ({ panel }) => {
  const [wires, setWires] = useState<Wire[]>([]);
  const [panelSlots, setPanelSlots] = useState<PanelSlot[]>([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingWire, setEditingWire] = useState<Wire | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [colorStandards, setColorStandards] = useState<any>({});
  const [crossSectionStandards, setCrossSectionStandards] = useState<any[]>([]);
  
  const [formData, setFormData] = useState<WireFormData>({
    label: '',
    wire_type: 'Live',
    cross_section: 2.5,
    color: '',
    source_slot_id: '',
    destination_slot_id: '',
    external_source: '',
    external_destination: '',
    length: '',
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        
        // Fetch wiring data
        const wiringResponse = await wiringAPI.getPanelWiring(panel.id);
        setWires(wiringResponse.data);
        
        // Fetch panel details
        const panelResponse = await panelAPI.getPanel(panel.id);
        setPanelSlots(panelResponse.data.slots || []);
        
        // Fetch standards
        const [colorsResponse, crossSectionsResponse] = await Promise.all([
          wiringAPI.getWireColorStandards(),
          wiringAPI.getWireCrossSectionStandards(),
        ]);
        setColorStandards(colorsResponse.data);
        setCrossSectionStandards(crossSectionsResponse.data.domestic || []);
        
      } catch (err) {
        setError('Failed to fetch data');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [panel.id]);

  const handleOpenDialog = (wire?: Wire) => {
    if (wire) {
      setEditingWire(wire);
      setFormData({
        label: wire.label,
        wire_type: wire.wire_type,
        cross_section: wire.cross_section,
        color: wire.color || '',
        source_slot_id: wire.source_slot_id || '',
        destination_slot_id: wire.destination_slot_id || '',
        external_source: wire.external_source || '',
        external_destination: wire.external_destination || '',
        length: wire.length || '',
      });
    } else {
      setEditingWire(null);
      setFormData({
        label: '',
        wire_type: 'Live',
        cross_section: 2.5,
        color: '',
        source_slot_id: '',
        destination_slot_id: '',
        external_source: '',
        external_destination: '',
        length: '',
      });
    }
    setDialogOpen(true);
  };

  const handleSaveWire = async () => {
    try {
      const wireData: WireCreate = {
        panel_id: panel.id,
        label: formData.label,
        wire_type: formData.wire_type,
        cross_section: formData.cross_section,
        color: formData.color || undefined,
        source_slot_id: formData.source_slot_id || undefined,
        destination_slot_id: formData.destination_slot_id || undefined,
        external_source: formData.external_source || undefined,
        external_destination: formData.external_destination || undefined,
        length: formData.length ? Number(formData.length) : undefined,
      };

      if (editingWire) {
        const response = await wiringAPI.updateWire(editingWire.id, wireData);
        setWires(wires.map(w => w.id === editingWire.id ? response.data : w));
      } else {
        const response = await wiringAPI.createWire(wireData);
        setWires([...wires, response.data]);
      }

      setDialogOpen(false);
      setEditingWire(null);
    } catch (err) {
      setError('Failed to save wire');
      console.error('Error saving wire:', err);
    }
  };

  const handleDeleteWire = async (wireId: number) => {
    if (!window.confirm('Are you sure you want to delete this wire?')) return;

    try {
      await wiringAPI.deleteWire(wireId);
      setWires(wires.filter(w => w.id !== wireId));
    } catch (err) {
      setError('Failed to delete wire');
      console.error('Error deleting wire:', err);
    }
  };

  const getSlotLabel = (slotId: number) => {
    const slot = panelSlots.find(s => s.id === slotId);
    if (!slot) return `Slot ${slotId}`;
    
    if (slot.device_label) return `${slot.slot_number}: ${slot.device_label}`;
    if (slot.device_template) return `${slot.slot_number}: ${slot.device_template.name}`;
    return `Slot ${slot.slot_number}`;
  };

  const getWireTypeColor = (wireType: string) => {
    switch (wireType.toLowerCase()) {
      case 'live': return 'error';
      case 'neutral': return 'primary';
      case 'earth': return 'success';
      default: return 'default';
    }
  };

  const occupiedSlots = panelSlots.filter(slot => slot.is_occupied);

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Typography>Loading wiring configuration...</Typography>
      ) : (
        <>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6">
              Wiring Configuration
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog()}
            >
              Add Wire
            </Button>
          </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12 }}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Label</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Cross Section</TableCell>
                  <TableCell>Color</TableCell>
                  <TableCell>From</TableCell>
                  <TableCell>To</TableCell>
                  <TableCell>Length</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {wires.map((wire) => (
                  <TableRow key={wire.id}>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CableIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        {wire.label}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={wire.wire_type} 
                        size="small" 
                        color={getWireTypeColor(wire.wire_type) as any}
                      />
                    </TableCell>
                    <TableCell>{wire.cross_section}mm²</TableCell>
                    <TableCell>
                      {wire.color && (
                        <Chip
                          label={wire.color}
                          size="small"
                          sx={{
                            backgroundColor: wire.color.toLowerCase() === 'brown' ? '#8B4513' :
                                             wire.color.toLowerCase() === 'blue' ? '#0000FF' :
                                             wire.color.toLowerCase() === 'green/yellow' ? '#32CD32' :
                                             '#gray',
                            color: 'white',
                          }}
                        />
                      )}
                    </TableCell>
                    <TableCell>
                      {wire.source_slot_id ? getSlotLabel(wire.source_slot_id) : wire.external_source}
                    </TableCell>
                    <TableCell>
                      {wire.destination_slot_id ? getSlotLabel(wire.destination_slot_id) : wire.external_destination}
                    </TableCell>
                    <TableCell>
                      {wire.length ? `${wire.length}m` : '-'}
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => handleOpenDialog(wire)}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteWire(wire.id)}
                        color="error"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {wires.length === 0 && (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="body1" color="text.secondary">
                No wiring connections configured yet.
              </Typography>
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={() => handleOpenDialog()}
                sx={{ mt: 2 }}
              >
                Add Your First Wire
              </Button>
            </Box>
          )}
        </Grid>
      </Grid>

      {/* Wire Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingWire ? 'Edit Wire' : 'Add New Wire'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ pt: 1 }}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                label="Wire Label"
                value={formData.label}
                onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                fullWidth
                required
                placeholder="e.g., Kitchen Lights L1"
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                select
                label="Wire Type"
                value={formData.wire_type}
                onChange={(e) => setFormData({ ...formData, wire_type: e.target.value })}
                fullWidth
                required
              >
                <MenuItem value="Live">Live</MenuItem>
                <MenuItem value="Neutral">Neutral</MenuItem>
                <MenuItem value="Earth">Earth</MenuItem>
                <MenuItem value="Switched Live">Switched Live</MenuItem>
                <MenuItem value="Data">Data</MenuItem>
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                select
                label="Cross Section"
                value={formData.cross_section}
                onChange={(e) => setFormData({ ...formData, cross_section: parseFloat(e.target.value) })}
                fullWidth
                required
              >
                {crossSectionStandards.map((standard) => (
                  <MenuItem key={standard.cross_section} value={standard.cross_section}>
                    {standard.cross_section}mm² ({standard.current} - {standard.typical_use})
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                select
                label="Wire Color"
                value={formData.color}
                onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                fullWidth
              >
                <MenuItem value="">Select color...</MenuItem>
                {colorStandards.UK && Object.entries(colorStandards.UK).map(([type, colors]) => (
                  (colors as string[]).map((color) => (
                    <MenuItem key={`${type}-${color}`} value={color}>
                      {color} ({type})
                    </MenuItem>
                  ))
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                select
                label="Source (From)"
                value={formData.source_slot_id}
                onChange={(e) => setFormData({ ...formData, source_slot_id: Number(e.target.value) })}
                fullWidth
              >
                <MenuItem value="">External/Manual</MenuItem>
                {occupiedSlots.map((slot) => (
                  <MenuItem key={slot.id} value={slot.id}>
                    {getSlotLabel(slot.id)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                select
                label="Destination (To)"
                value={formData.destination_slot_id}
                onChange={(e) => setFormData({ ...formData, destination_slot_id: Number(e.target.value) })}
                fullWidth
              >
                <MenuItem value="">External/Manual</MenuItem>
                {occupiedSlots.map((slot) => (
                  <MenuItem key={slot.id} value={slot.id}>
                    {getSlotLabel(slot.id)}
                  </MenuItem>
                ))}
              </TextField>
            </Grid>
            {!formData.source_slot_id && (
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField
                  label="External Source"
                  value={formData.external_source}
                  onChange={(e) => setFormData({ ...formData, external_source: e.target.value })}
                  fullWidth
                  placeholder="e.g., Main Supply, Distribution Board"
                />
              </Grid>
            )}
            {!formData.destination_slot_id && (
              <Grid size={{ xs: 12, sm: 6 }}>
                <TextField
                  label="External Destination"
                  value={formData.external_destination}
                  onChange={(e) => setFormData({ ...formData, external_destination: e.target.value })}
                  fullWidth
                  placeholder="e.g., Kitchen Outlets, Living Room Lights"
                />
              </Grid>
            )}
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField
                label="Length (meters)"
                type="number"
                value={formData.length}
                onChange={(e) => setFormData({ ...formData, length: e.target.value as any })}
                fullWidth
                placeholder="Optional"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveWire} variant="contained">
            {editingWire ? 'Update' : 'Create'} Wire
          </Button>
        </DialogActions>
      </Dialog>
        </>
      )}
    </Box>
  );
};

export default WiringView;
