import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
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
import { panelAPI, templateAPI } from '../services/api';

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
  const [selectedTemplate, setSelectedTemplate] = useState<number | ''>('');
  const [newPanel, setNewPanel] = useState<PanelCreate>({
    name: '',
    template_id: 0,
    location: '',
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
      const response = await templateAPI.getPanelLibrary();
      setTemplates(response.data);
    } catch (err) {
      console.error('Error fetching templates:', err);
    }
  };

  const handleCreatePanel = async () => {
    if (!selectedTemplate) {
      setError('Please select a template');
      return;
    }
    
    try {
      setLoading(true);
      const panelData = {
        ...newPanel,
        template_id: selectedTemplate as number,
      };
      const response = await panelAPI.createPanel(panelData);
      const createdPanel = response.data;
      setPanels([...panels, createdPanel]);
      setDialogOpen(false);
      onPanelSelect(createdPanel);
      setSelectedTemplate('');
      setNewPanel({
        name: '',
        template_id: 0,
        location: '',
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
                secondary={panel.template ? 
                  `${panel.template.model} - ${panel.template.total_slots} slots (${panel.template.rows}×${panel.template.slots_per_row})` :
                  'Template information not available'
                }
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
        <DialogTitle>Create New Panel Instance</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              label="Panel Name"
              value={newPanel.name}
              onChange={(e) => setNewPanel({ ...newPanel, name: e.target.value })}
              fullWidth
              required
              placeholder="e.g., Main Distribution Board, Kitchen Panel"
            />
            
            <TextField
              select
              label="Panel Template"
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(Number(e.target.value))}
              fullWidth
              required
              helperText="Select a pre-configured panel template"
            >
              <MenuItem value="">Choose a template...</MenuItem>
              {templates.map((template) => (
                <MenuItem key={template.id} value={template.id}>
                  {template.name} - {template.model} ({template.rows}×{template.slots_per_row} slots)
                </MenuItem>
              ))}
            </TextField>
            
            {selectedTemplate && (
              <Box sx={{ p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Template Details:
                </Typography>
                {(() => {
                  const template = templates.find(t => t.id === selectedTemplate);
                  if (!template) return null;
                  return (
                    <Typography variant="body2" color="text.secondary">
                      {template.manufacturer} {template.model} - {template.total_slots} slots 
                      ({template.rows} rows × {template.slots_per_row} slots), 
                      {template.voltage}V, {template.max_current}A
                      {template.description && <><br/>{template.description}</>}
                    </Typography>
                  );
                })()}
              </Box>
            )}
            
            <TextField
              label="Location (Optional)"
              value={newPanel.location || ''}
              onChange={(e) => setNewPanel({ ...newPanel, location: e.target.value })}
              fullWidth
              placeholder="e.g., Basement, Kitchen, Main Floor"
            />
            
            <TextField
              label="Description (Optional)"
              value={newPanel.description || ''}
              onChange={(e) => setNewPanel({ ...newPanel, description: e.target.value })}
              fullWidth
              multiline
              rows={3}
              placeholder="Additional notes about this panel installation"
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
                        {template.rows * template.slots_per_row} slots ({template.rows} rows × {template.slots_per_row} slots), {template.voltage}V, {template.max_current}A
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
