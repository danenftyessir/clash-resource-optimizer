import os
import pandas as pd
import numpy as np

def load_game_data():
    """Load dan validasi semua data game dari file CSV"""
    try:
        # Dapatkan absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        
        # Print paths untuk debugging
        print("Debugging file paths:")
        print(f"Current directory: {current_dir}")
        print(f"Parent directory: {parent_dir}")
        
        # Konstruksi full path dengan nama file yang benar
        buildings_path = os.path.join(parent_dir, 'data', 'th11_building.csv')
        upgrades_path = os.path.join(parent_dir, 'data', 'upgrade_cost.csv')
        production_path = os.path.join(parent_dir, 'data', 'production_rates.csv')
        
        # Log lokasi file
        print(f"\nLooking for files at:")
        print(f"Buildings: {buildings_path}")
        print(f"Upgrades: {upgrades_path}")
        print(f"Production: {production_path}")
        
        # Cek keberadaan file
        print("\nFile existence check:")
        print(f"Buildings exists: {os.path.exists(buildings_path)}")
        print(f"Upgrades exists: {os.path.exists(upgrades_path)}")
        print(f"Production exists: {os.path.exists(production_path)}")
        
        # Validasi keberadaan semua file yang dibutuhkan
        if not all(os.path.exists(p) for p in [buildings_path, upgrades_path, production_path]):
            raise FileNotFoundError("One or more required files are missing")
            
        # Load semua file CSV
        buildings = pd.read_csv(buildings_path)
        upgrades = pd.read_csv(upgrades_path)
        production = pd.read_csv(production_path)
        
        # Print sample data untuk verifikasi
        print("\nSample data:")
        print("\nBuildings:")
        print(buildings.head())
        print("\nUpgrades:")
        print(upgrades.head())
        print("\nProduction:")
        print(production.head())
        return buildings, upgrades, production
    except Exception as e:
        print(f"\nError: {str(e)}")
        return None

def calculate_build_time(upgrade_tasks, num_builders):
    """Menghitung waktu build optimal dengan multiple builders"""
    if not upgrade_tasks:
        return 0
    
    # Konversi tasks ke array waktu
    times = sorted([task['time_hours'] for task in upgrade_tasks], reverse=True)
    
    # Inisialisasi queue builder
    builder_queues = [0] * num_builders
    
    # Assign tasks ke builders
    for time in times:
        # Cari builder dengan waktu kerja minimum
        min_queue = min(builder_queues)
        idx = builder_queues.index(min_queue)
        builder_queues[idx] += time
    
    # Total waktu adalah queue terpanjang
    return max(builder_queues)