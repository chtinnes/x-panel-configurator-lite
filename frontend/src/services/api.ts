import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Template API (new)
export const templateAPI = {
  // Panel Templates
  getPanelTemplates: (manufacturer?: string, series?: string) => 
    api.get('/templates/panel-templates', { 
      params: { manufacturer, series, active_only: true } 
    }),
  getPanelTemplate: (id: number) => api.get(`/templates/panel-templates/${id}`),
  createPanelTemplate: (template: any) => api.post('/templates/panel-templates', template),
  updatePanelTemplate: (id: number, template: any) => api.put(`/templates/panel-templates/${id}`, template),
  deletePanelTemplate: (id: number) => api.delete(`/templates/panel-templates/${id}`),
  
  // Device Templates
  getDeviceTemplates: (manufacturer?: string, series?: string, deviceType?: string, category?: string) => 
    api.get('/templates/device-templates', { 
      params: { manufacturer, series, device_type: deviceType, category, active_only: true } 
    }),
  getDeviceTemplate: (id: number) => api.get(`/templates/device-templates/${id}`),
  createDeviceTemplate: (template: any) => api.post('/templates/device-templates', template),
  updateDeviceTemplate: (id: number, template: any) => api.put(`/templates/device-templates/${id}`, template),
  deleteDeviceTemplate: (id: number) => api.delete(`/templates/device-templates/${id}`),
  
  // Library endpoints
  getDeviceLibrary: (manufacturer: string = 'hager', category?: string) => 
    api.get(`/templates/library/devices/${manufacturer}`, { params: { category } }),
  getPanelLibrary: (manufacturer: string = 'hager', series?: string) => 
    api.get(`/templates/library/panels/${manufacturer}`, { params: { series } }),
};

// Panel API (updated for template system)
export const panelAPI = {
  getAllPanels: () => api.get('/panels/'),
  getPanel: (id: number) => api.get(`/panels/${id}`),
  createPanel: (panel: any) => api.post('/panels/', panel),
  updatePanel: (id: number, panel: any) => api.put(`/panels/${id}`, panel),
  deletePanel: (id: number) => api.delete(`/panels/${id}`),
  
  // Legacy template endpoint (redirects to template API)
  getHagerVoltaTemplates: () => templateAPI.getPanelLibrary('hager', 'volta'),
};

// Device API (updated for template system)  
export const deviceAPI = {
  // Legacy endpoints (still available but deprecated)
  getAllDeviceTypes: () => api.get('/devices/types'),
  getDeviceType: (id: number) => api.get(`/devices/types/${id}`),
  createDeviceType: (device: any) => api.post('/devices/types', device),
  
  // Slot management (now uses device_template_id)
  updatePanelSlot: (slotId: number, slot: any) => api.put(`/devices/slots/${slotId}`, slot),
  removeDeviceFromSlot: (slotId: number) => api.delete(`/devices/slots/${slotId}/device`),
  canPlaceDevice: (slotId: number, deviceTemplateId: number) => 
    api.get(`/devices/slots/${slotId}/can-place/${deviceTemplateId}`),
  
  // Library endpoint (now redirects to template API)
  getHagerDeviceLibrary: () => templateAPI.getDeviceLibrary('hager'),
};

// Wiring API (unchanged)
export const wiringAPI = {
  getPanelWiring: (panelId: number) => api.get(`/wiring/panel/${panelId}`),
  getWire: (id: number) => api.get(`/wiring/${id}`),
  createWire: (wire: any) => api.post('/wiring/', wire),
  updateWire: (id: number, wire: any) => api.put(`/wiring/${id}`, wire),
  deleteWire: (id: number) => api.delete(`/wiring/${id}`),
  getWireColorStandards: () => api.get('/wiring/standards/colors'),
  getWireCrossSectionStandards: () => api.get('/wiring/standards/cross-sections'),
};

export default api;
