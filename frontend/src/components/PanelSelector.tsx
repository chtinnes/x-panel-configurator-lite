import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Typography,
  Alert,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { Panel, PanelTemplate, PanelCreate } from '../types';
import { panelAPI } from '../services/api';

interface PanelSelectorProps {
  onPanelSelect: (panel: Panel) => void;
}

const PanelSelector: React.FC<PanelSelectorProps> = ({ onPanelSelect }) => {
  const [panels, setPanels] = useState<Panel[]>([]);
  const [templates, setTemplates] = useState<PanelTemplate[]>([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [templateDialogOpen, setTemplateDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newPanel, setNewPanel] = useState<PanelCreate>({
    name: '',
    model: '',
    manufacturer: 'Hager',
    rows: 2,
    slots_per_row: 6,
    voltage: 230,
    current_rating: 63,
    description: '',
  });

  useEffect(() => {
    fetchPanels();
    fetchTemplates();
  }, []);

  const fetchPanels = async () => {
    try {
      setLoading(true);
      const response = await panelAPI.getAllPanels();
      setPanels(response.data);
    } catch (err) {
      setError('Failed to fetch panels');
      console.error('Error fetching panels:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await panelAPI.getHagerVoltaTemplates();
      setTemplates(response.data);
    } catch (err) {
      console.error('Error fetching templates:', err);
    }
  };

  const handleCreatePanel = async () => {
    try {
      setLoading(true);
      const response = await panelAPI.createPanel(newPanel);
      const createdPanel = response.data;
      setPanels([...panels, createdPanel]);
      setDialogOpen(false);
      onPanelSelect(createdPanel);
      setNewPanel({
        name: '',
        model: '',
        manufacturer: 'Hager',
        rows: 2,
        slots_per_row: 6,
        voltage: 230,
        current_rating: 63,
        description: '',
      });
    } catch (err) {
      setError('Failed to create panel');
      console.error('Error creating panel:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFromTemplate = async (template: PanelTemplate) => {
    try {
      setLoading(true);
      const panelData = { ...template, name: `${template.name} - ${Date.now()}` };
      const response = await panelAPI.createPanel(panelData);
      const createdPanel = response.data;
      setPanels([...panels, createdPanel]);
      setTemplateDialogOpen(false);
      onPanelSelect(createdPanel);
    } catch (err) {
      setError('Failed to create panel from template');
      console.error('Error creating panel from template:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePanel = async (panelId: number) => {
    if (!window.confirm('Are you sure you want to delete this panel?')) return;
    
    try {
      await panelAPI.deletePanel(panelId);
      setPanels(panels.filter(p => p.id !== panelId));
    } catch (err) {
      setError('Failed to delete panel');
      console.error('Error deleting panel:', err);
    }
  };

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      
      <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setDialogOpen(true)}
          size="small"
        >
          Create Panel
        </Button>
        <Button
          variant="outlined"
          onClick={() => setTemplateDialogOpen(true)}
          size="small"
        >
          From Template
        </Button>
      </Box>        <List dense>
        {panels.map((panel) => (
          <ListItem
            key={panel.id}
            disablePadding
            sx={{
              border: '1px solid #ddd',
              borderRadius: 1,
              mb: 1,
            }}
          >
            <ListItemButton onClick={() => onPanelSelect(panel)}>
              <ListItemText
                primary={panel.name}
                secondary={`${panel.model} - ${panel.total_slots} slots (${panel.rows}×${panel.slots_per_row})`}
              />
            </ListItemButton>
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeletePanel(panel.id);
                }}
                size="small"
              >
                <DeleteIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>

      {/* Create Panel Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Panel</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="Panel Name"
              value={newPanel.name}
              onChange={(e) => setNewPanel({ ...newPanel, name: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Model"
              value={newPanel.model}
              onChange={(e) => setNewPanel({ ...newPanel, model: e.target.value })}
              fullWidth
              required
            />
            <TextField
              label="Manufacturer"
              value={newPanel.manufacturer}
              onChange={(e) => setNewPanel({ ...newPanel, manufacturer: e.target.value })}
              fullWidth
            />
            <TextField
              label="Number of Rows"
              type="number"
              value={newPanel.rows}
              onChange={(e) => setNewPanel({ ...newPanel, rows: parseInt(e.target.value) })}
              fullWidth
              required
              inputProps={{ min: 1, max: 4 }}
              helperText="Typically 2-3 rows for standard panels"
            />
            <TextField
              label="Slots per Row"
              type="number"
              value={newPanel.slots_per_row}
              onChange={(e) => setNewPanel({ ...newPanel, slots_per_row: parseInt(e.target.value) })}
              fullWidth
              required
              inputProps={{ min: 1, max: 12 }}
              helperText="Number of devices that fit in one row"
            />
            <TextField
              label="Total Slots"
              value={newPanel.rows * newPanel.slots_per_row}
              fullWidth
              disabled
              helperText="Automatically calculated from rows × slots per row"
            />
            <TextField
              label="Number of Rows"
              type="number"
              value={newPanel.rows}
              onChange={(e) => setNewPanel({ ...newPanel, rows: parseInt(e.target.value) })}
              fullWidth
              required
              helperText="How many horizontal rows of devices"
            />
            <TextField
              label="Slots per Row"
              type="number"
              value={newPanel.slots_per_row}
              onChange={(e) => setNewPanel({ ...newPanel, slots_per_row: parseInt(e.target.value) })}
              fullWidth
              required
              helperText="How many device slots in each row"
            />
            <TextField
              label="Voltage (V)"
              type="number"
              value={newPanel.voltage}
              onChange={(e) => setNewPanel({ ...newPanel, voltage: parseFloat(e.target.value) })}
              fullWidth
              required
            />
            <TextField
              label="Current Rating (A)"
              type="number"
              value={newPanel.current_rating}
              onChange={(e) => setNewPanel({ ...newPanel, current_rating: parseFloat(e.target.value) })}
              fullWidth
              required
            />
            <TextField
              label="Description"
              value={newPanel.description}
              onChange={(e) => setNewPanel({ ...newPanel, description: e.target.value })}
              fullWidth
              multiline
              rows={2}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCreatePanel} variant="contained" disabled={loading}>
            Create
          </Button>
        </DialogActions>
      </Dialog>

      {/* Template Dialog */}
      <Dialog open={templateDialogOpen} onClose={() => setTemplateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Select Panel Template</DialogTitle>
        <DialogContent>
          <List>
            {templates.map((template, index) => (
              <ListItem
                key={index}
                disablePadding
                sx={{
                  border: '1px solid #ddd',
                  borderRadius: 1,
                  mb: 1,
                }}
              >
                <ListItemButton onClick={() => handleCreateFromTemplate(template)}>
                  <ListItemText
                    primary={template.name}
                    secondary={
                      <Typography component="span" variant="body2">
                        {template.description}<br />
                        {template.rows * template.slots_per_row} slots ({template.rows} rows × {template.slots_per_row} slots), {template.voltage}V, {template.current_rating}A
                      </Typography>
                    }
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTemplateDialogOpen(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PanelSelector;
