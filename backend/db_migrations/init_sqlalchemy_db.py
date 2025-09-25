#!/usr/bin/env python3
"""
Initialize database using SQLAlchemy models and seed with template data.
"""

from database import SessionLocal, engine, Base
from models import PanelTemplate, DeviceTemplate, Panel, PanelSlot
from datetime import datetime

def create_database():
    """Create database tables using SQLAlchemy"""
    print("🏗️  Creating database tables with SQLAlchemy...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def seed_templates():
    """Seed template data"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding template data...")
        
        # Check if templates already exist
        existing_panel_templates = db.query(PanelTemplate).count()
        if existing_panel_templates > 0:
            print(f"ℹ️  Found {existing_panel_templates} existing panel templates, skipping seeding")
            return
        
        # Seed panel templates
        panel_templates = [
            PanelTemplate(
                name='Hager Volta 12-way Consumer Unit',
                model='VML712',
                manufacturer='Hager',
                series='Volta',
                rows=2,
                slots_per_row=6,
                voltage=230,
                max_current=100,
                enclosure_type='Metal',
                protection_rating='IP30',
                description='Standard 12-way consumer unit for residential installations',
                is_active=True
            ),
            PanelTemplate(
                name='Hager Volta 18-way Consumer Unit',
                model='VML718',
                manufacturer='Hager',
                series='Volta',
                rows=3,
                slots_per_row=6,
                voltage=230,
                max_current=100,
                enclosure_type='Metal',
                protection_rating='IP30',
                description='18-way consumer unit for larger residential installations',
                is_active=True
            ),
            PanelTemplate(
                name='Hager Volta 24-way Consumer Unit',
                model='VML724',
                manufacturer='Hager',
                series='Volta',
                rows=4,
                slots_per_row=6,
                voltage=230,
                max_current=100,
                enclosure_type='Metal',
                protection_rating='IP30',
                description='24-way consumer unit for larger residential installations',
                is_active=True
            ),
            PanelTemplate(
                name='Hager Volta 36-way Consumer Unit',
                model='VML736',
                manufacturer='Hager',
                series='Volta',
                rows=6,
                slots_per_row=6,
                voltage=230,
                max_current=100,
                enclosure_type='Metal',
                protection_rating='IP30',
                description='36-way consumer unit for large residential/commercial installations',
                is_active=True
            ),
            PanelTemplate(
                name='Hager Volta 48-way Consumer Unit',
                model='VML748',
                manufacturer='Hager',
                series='Volta',
                rows=8,
                slots_per_row=6,
                voltage=230,
                max_current=100,
                enclosure_type='Metal',
                protection_rating='IP30',
                description='48-way consumer unit for large commercial installations',
                is_active=True
            )
        ]
        
        for template in panel_templates:
            db.add(template)
        
        # Seed device templates
        device_templates = [
            # MCBs - Type B Curve
            DeviceTemplate(
                name='Single Pole MCB 6A Type B',
                model='MTN106',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=6,
                max_current=6,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='B',
                pole_count=1,
                width_in_modules=1,
                description='6A Type B single pole MCB for lighting circuits',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 10A Type B',
                model='MTN110',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=10,
                max_current=10,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='B',
                pole_count=1,
                width_in_modules=1,
                description='10A Type B single pole MCB for lighting circuits',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 16A Type B',
                model='MTN116',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=16,
                max_current=16,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='B',
                pole_count=1,
                width_in_modules=1,
                description='16A Type B single pole MCB for socket outlets',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 20A Type B',
                model='MTN120',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=20,
                max_current=20,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='B',
                pole_count=1,
                width_in_modules=1,
                description='20A Type B single pole MCB for socket outlets',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 32A Type B',
                model='MTN132',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=32,
                max_current=32,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='B',
                pole_count=1,
                width_in_modules=1,
                description='32A Type B single pole MCB for high power circuits',
                is_active=True
            ),
            # MCBs - Type C Curve
            DeviceTemplate(
                name='Single Pole MCB 16A Type C',
                model='MTN116C',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=16,
                max_current=16,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='C',
                pole_count=1,
                width_in_modules=1,
                description='16A Type C single pole MCB for motor circuits',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 20A Type C',
                model='MTN120C',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=20,
                max_current=20,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='C',
                pole_count=1,
                width_in_modules=1,
                description='20A Type C single pole MCB for motor circuits',
                is_active=True
            ),
            DeviceTemplate(
                name='Single Pole MCB 32A Type C',
                model='MTN132C',
                manufacturer='Hager',
                series='MyTN',
                device_type='MCB',
                category='Protection',
                slots_required=1,
                rated_current=32,
                max_current=32,
                voltage_range='230V AC',
                breaking_capacity=6000,
                curve_type='C',
                pole_count=1,
                width_in_modules=1,
                description='32A Type C single pole MCB for motor circuits',
                is_active=True
            ),
            # RCDs
            DeviceTemplate(
                name='30mA RCD 63A Double Pole',
                model='CDC263D',
                manufacturer='Hager',
                series='CDC',
                device_type='RCD',
                category='Protection',
                slots_required=2,
                rated_current=63,
                max_current=63,
                voltage_range='230V AC',
                sensitivity=30,
                pole_count=2,
                width_in_modules=2,
                description='30mA RCD for earth leakage protection',
                is_active=True
            ),
            DeviceTemplate(
                name='100mA RCD 63A Double Pole',
                model='CDC263S',
                manufacturer='Hager',
                series='CDC',
                device_type='RCD',
                category='Protection',
                slots_required=2,
                rated_current=63,
                max_current=63,
                voltage_range='230V AC',
                sensitivity=100,
                pole_count=2,
                width_in_modules=2,
                description='100mA RCD for fire protection',
                is_active=True
            ),
            # RCBOs
            DeviceTemplate(
                name='RCBO 16A Type B 30mA',
                model='ADS116D',
                manufacturer='Hager',
                series='ADS',
                device_type='RCBO',
                category='Protection',
                slots_required=2,
                rated_current=16,
                max_current=16,
                voltage_range='230V AC',
                breaking_capacity=6000,
                sensitivity=30,
                curve_type='B',
                pole_count=1,
                width_in_modules=2,
                description='16A Type B RCBO with 30mA RCD protection',
                is_active=True
            ),
            DeviceTemplate(
                name='RCBO 20A Type B 30mA',
                model='ADS120D',
                manufacturer='Hager',
                series='ADS',
                device_type='RCBO',
                category='Protection',
                slots_required=2,
                rated_current=20,
                max_current=20,
                voltage_range='230V AC',
                breaking_capacity=6000,
                sensitivity=30,
                curve_type='B',
                pole_count=1,
                width_in_modules=2,
                description='20A Type B RCBO with 30mA RCD protection',
                is_active=True
            ),
            DeviceTemplate(
                name='RCBO 32A Type B 30mA',
                model='ADS132D',
                manufacturer='Hager',
                series='ADS',
                device_type='RCBO',
                category='Protection',
                slots_required=2,
                rated_current=32,
                max_current=32,
                voltage_range='230V AC',
                breaking_capacity=6000,
                sensitivity=30,
                curve_type='B',
                pole_count=1,
                width_in_modules=2,
                description='32A Type B RCBO with 30mA RCD protection',
                is_active=True
            ),
            # Smart Meter
            DeviceTemplate(
                name='Digital Smart Meter',
                model='EHM310',
                manufacturer='Hager',
                series='EHM',
                device_type='Smart Meter',
                category='Measurement',
                slots_required=4,
                rated_current=100,
                max_current=100,
                voltage_range='230V AC',
                pole_count=3,
                width_in_modules=4,
                features='LCD display, Energy monitoring, Remote reading capability',
                description='Digital electricity meter with smart monitoring capabilities',
                is_active=True
            ),
            # Contactors
            DeviceTemplate(
                name='Modular Contactor 25A 2NO',
                model='ERC225',
                manufacturer='Hager',
                series='ERC',
                device_type='Contactor',
                category='Control',
                slots_required=2,
                rated_current=25,
                max_current=25,
                voltage_range='230V AC',
                pole_count=2,
                width_in_modules=2,
                description='25A 2-pole normally open modular contactor',
                is_active=True
            ),
            # Timers
            DeviceTemplate(
                name='Digital Time Switch',
                model='EG203B',
                manufacturer='Hager',
                series='EG',
                device_type='Timer',
                category='Control',
                slots_required=2,
                rated_current=16,
                max_current=16,
                voltage_range='230V AC',
                width_in_modules=2,
                features='7-day programming, LCD display, Multiple switching times',
                description='Digital time switch for automated control',
                is_active=True
            ),
            # Surge Protection
            DeviceTemplate(
                name='Surge Protection Device Type 2',
                model='SPN415',
                manufacturer='Hager',
                series='SPN',
                device_type='SPD',
                category='Protection',
                slots_required=2,
                voltage_range='230V AC',
                width_in_modules=2,
                description='Type 2 surge protection device',
                is_active=True
            )
        ]
        
        for template in device_templates:
            db.add(template)
        
        db.commit()
        print(f"✅ Seeded {len(panel_templates)} panel templates and {len(device_templates)} device templates")
        
    except Exception as e:
        print(f"❌ Template seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    print("🚀 Initializing database with SQLAlchemy...")
    
    # Step 1: Create database tables
    create_database()
    
    # Step 2: Seed template data
    seed_templates()
    
    print("\n🎉 Database initialization complete!")
    print("📋 Summary:")
    print("   ✅ Database tables created with SQLAlchemy")
    print("   ✅ Panel and device templates seeded")
    print("   🔄 You can now start the backend server")

if __name__ == "__main__":
    main()