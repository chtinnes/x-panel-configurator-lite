// Template interfaces (reusable specifications)
export interface PanelTemplate {
  id: number;
  name: string;
  model: string;
  manufacturer: string;
  series?: string;
  rows: number;
  slots_per_row: number;
  total_slots: number; // Computed from rows * slots_per_row
  voltage: number;
  max_current: number;
  enclosure_type?: string;
  protection_rating?: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PanelTemplateCreate {
  name: string;
  model: string;
  manufacturer: string;
  series?: string;
  rows: number;
  slots_per_row: number;
  voltage: number;
  max_current: number;
  enclosure_type?: string;
  protection_rating?: string;
  description?: string;
  is_active?: boolean;
}

export interface DeviceTemplate {
  id: number;
  name: string;
  model: string;
  manufacturer: string;
  series?: string;
  device_type: string; // MCB, RCD, RCBO, Smart Meter
  category: string;     // Protection, Measurement, Control
  slots_required: number;
  rated_current?: number;
  max_current?: number;
  voltage_range?: string;
  breaking_capacity?: number;
  sensitivity?: number;
  curve_type?: string;
  pole_count?: number;
  width_in_modules: number;
  mounting_type?: string;
  features?: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface DeviceTemplateCreate {
  name: string;
  model: string;
  manufacturer: string;
  series?: string;
  device_type: string;
  category: string;
  slots_required?: number;
  rated_current?: number;
  max_current?: number;
  voltage_range?: string;
  breaking_capacity?: number;
  sensitivity?: number;
  curve_type?: string;
  pole_count?: number;
  width_in_modules?: number;
  mounting_type?: string;
  features?: string;
  description?: string;
  is_active?: boolean;
}

// Instance interfaces (actual installations)
export interface Panel {
  id: number;
  name: string;
  template_id: number;
  location?: string;
  installation_date?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
  template?: PanelTemplate;
  slots?: PanelSlot[];
}

export interface PanelCreate {
  name: string;
  template_id: number;
  location?: string;
  installation_date?: string;
  description?: string;
}

export interface PanelSlot {
  id: number;
  panel_id: number;
  slot_number: number;
  row: number;
  column: number;
  device_template_id?: number | null;
  device_label?: string;
  current_setting?: number;
  custom_properties?: string;
  is_occupied: boolean;
  spans_slots: number;
  installed_date?: string;
  device_template?: DeviceTemplate;
  input_wires?: Wire[];
  output_wires?: Wire[];
}

export interface PanelSlotUpdate {
  device_template_id?: number | null;
  device_label?: string;
  current_setting?: number;
  custom_properties?: string;
  spans_slots?: number;
  installed_date?: string;
}

export interface Wire {
  id: number;
  panel_id: number;
  label: string;
  wire_type: string;
  cross_section: number;
  color?: string;
  source_slot_id?: number;
  destination_slot_id?: number;
  external_source?: string;
  external_destination?: string;
  length?: number;
}

export interface WireCreate {
  panel_id: number;
  label: string;
  wire_type: string;
  cross_section: number;
  color?: string;
  source_slot_id?: number;
  destination_slot_id?: number;
  external_source?: string;
  external_destination?: string;
  length?: number;
}

// Legacy interfaces (for backward compatibility)
export interface DeviceType {
  id: number;
  name: string;
  category: string;
  manufacturer: string;
  model: string;
  slots_required: number;
  max_current?: number;
  voltage_range?: string;
  description?: string;
}

export interface DeviceLibraryItem extends DeviceTemplate {
  // DeviceLibraryItem is now based on DeviceTemplate
}

// Utility interfaces for API responses
export interface LibraryResponse {
  devices: DeviceTemplate[];
  panels: PanelTemplate[];
}
