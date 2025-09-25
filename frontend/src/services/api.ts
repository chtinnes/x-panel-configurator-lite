import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Panel API
export const panelAPI = {
  getAllPanels: () => api.get('/panels/'),
  getPanel: (id: number) => api.get(`/panels/${id}`),
  createPanel: (panel: any) => api.post('/panels/', panel),
  updatePanel: (id: number, panel: any) => api.put(`/panels/${id}`, panel),
  deletePanel: (id: number) => api.delete(`/panels/${id}`),
  getHagerVoltaTemplates: () => api.get('/panels/templates/hager-volta'),
};

// Device API
export const deviceAPI = {
  getAllDeviceTypes: () => api.get('/devices/types'),
  getDeviceType: (id: number) => api.get(`/devices/types/${id}`),
  createDeviceType: (device: any) => api.post('/devices/types', device),
  updatePanelSlot: (slotId: number, slot: any) => api.put(`/devices/slots/${slotId}`, slot),
  removeDeviceFromSlot: (slotId: number) => api.delete(`/devices/slots/${slotId}/device`),
  getHagerDeviceLibrary: () => api.get('/devices/library/hager'),
  canPlaceDevice: (slotId: number, deviceTypeId: number) => 
    api.get(`/devices/slots/${slotId}/can-place/${deviceTypeId}`),
};

// Wiring API
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
