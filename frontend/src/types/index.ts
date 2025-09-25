export interface Panel {
  id: number;
  name: string;
  model: string;
  manufacturer: string;
  rows: number;
  slots_per_row: number;
  total_slots: number; // Computed from rows * slots_per_row
  voltage: number;
  current_rating: number;
  description?: string;
  created_at: string;
  updated_at?: string;
  slots?: PanelSlot[];
}

export interface PanelCreate {
  name: string;
  model: string;
  manufacturer: string;
  rows: number;
  slots_per_row: number;
  voltage: number;
  current_rating: number;
  description?: string;
}

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

export interface PanelSlot {
  id: number;
  panel_id: number;
  slot_number: number;
  row: number;
  column: number;
  device_type_id?: number | null;
  device_label?: string;
  current_setting?: number;
  is_occupied: boolean;
  spans_slots: number;
  device_type?: DeviceType;
  input_wires?: Wire[];
  output_wires?: Wire[];
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

export interface DeviceLibraryItem {
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

export interface PanelTemplate {
  name: string;
  model: string;
  manufacturer: string;
  rows: number;
  slots_per_row: number;
  voltage: number;
  current_rating: number;
  description?: string;
}
