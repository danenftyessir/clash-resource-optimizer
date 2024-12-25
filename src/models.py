import pandas as pd
import numpy as np

class ResourceOptimizer:
    def __init__(self, buildings, upgrades, production):
        # Inisialisasi data dasar dari CSV files
        self.buildings = buildings
        self.upgrades = upgrades
        self.production = production
        self.builders = 5  # Jumlah default builder di TH11

    # Fungsi helper untuk menghitung peningkatan produksi
    # Menggunakan relasi rekurens P(n) = P(n-1) + ΔP
    def _calculate_production_increase(self, upgrade):
        """Calculate production increase with proper validation"""
        try:
            # Ekstrak informasi upgrade
            building = upgrade['building']
            level = upgrade['level']
            
            if not any(x in building.lower() for x in ['mine', 'collector', 'drill']):
                return 0
                
            production_data = self.production.copy()
            building_prod = production_data[production_data['building'] == building]
            
            if building_prod.empty:
                return 0
                
            current_level = level - 1
            next_level = level
            current_rate = 0
            if current_level > 0:
                current_rates = building_prod[building_prod['level'] == current_level]
                if not current_rates.empty:
                    current_rate = current_rates['hourly_rate'].iloc[0]
            next_rates = building_prod[building_prod['level'] == next_level]
            if next_rates.empty:
                return 0
            next_rate = next_rates['hourly_rate'].iloc[0]
            return next_rate - current_rate
            
        except Exception as e:
            print(f"Error calculating production increase for {upgrade['building']}: {e}")
            return 0
        
    # Fungsi untuk menghitung ROI (Return on Investment)
    # Menggunakan relasi rekurens ROI(n) = ROI(n-1) * factor + benefit(n)
    def calculate_roi(self, upgrade, time_horizon=168): 
        """Calculate ROI with more differentiated values"""
        try:
            cost = upgrade['cost']
            building = upgrade['building']
            level = upgrade['level']
            building_info = self.buildings[self.buildings['building_name'] == building].iloc[0]
            category = building_info['category'].lower()
            benefit = 0
            if category == 'resource':
                # Production buildings
                production_increase = self._calculate_production_increase(upgrade)
                benefit = production_increase * time_horizon
                # Resource value multipliers
                multiplier = {
                    'dark': 5.0,    # Dark elixir highest value
                    'elixir': 2.0,  # Elixir medium value
                    'gold': 1.5     # Gold baseline value
                }
                resource_type = next((k for k in multiplier.keys() if k in building.lower()), 'gold')
                benefit *= multiplier[resource_type]
                # Hitung total benefit berdasarkan waktu
                benefit *= (0.85 ** (level - 1))
                
            elif category == 'storage':
                # Storage buildings 
                old_capacity = building_info['storage_capacity']
                new_capacity = old_capacity * (1.25 if level <= 6 else 1.15)  # Diminishing capacity increase
                capacity_increase = new_capacity - old_capacity
                # Storage value multipliers
                storage_value = {
                    'dark': 0.8,    # Dark elixir storage most important
                    'elixir': 0.5,  # Elixir storage medium importance
                    'gold': 0.4     # Gold storage baseline
                }
                # Tentukan tipe resource dari nama building
                resource_type = next((k for k in storage_value.keys() if k in building.lower()), 'gold')
                benefit = capacity_increase * storage_value[resource_type]
                benefit *= (1.1 ** (level - 1))
            
            elif category == 'defense':
                # Defense buildings
                defense_importance = {
                    'eagle': {'base': 0.8, 'scale': 0.95}, 
                    'inferno': {'base': 0.7, 'scale': 0.9},
                    'xbow': {'base': 0.6, 'scale': 0.85},
                    'tesla': {'base': 0.5, 'scale': 0.8},
                    'wizard': {'base': 0.4, 'scale': 0.75},
                    'archer': {'base': 0.35, 'scale': 0.7},
                    'cannon': {'base': 0.3, 'scale': 0.65},
                    'mortar': {'base': 0.25, 'scale': 0.6}
                }
                defense_type = next((k for k in defense_importance.keys() if k in building.lower()), 'cannon')
                stats = defense_importance[defense_type]
                # Hitung nilai benefit berdasarkan level
                base_value = stats['base'] * cost * 1.5
                scale_factor = stats['scale'] ** (level - 1)
                benefit = base_value * scale_factor
                # Tambahkan bonus untuk defense tertentu
                if defense_type in ['eagle', 'inferno']:
                    benefit *= 1.2
                    
            # Hitung ROI
            roi = ((benefit - cost) / cost * 100) if cost > 0 else 0
            bounds = {
                'resource': (15, 60),
                'storage': (5, 40), 
                'defense': (-25, 35)
            }
            
            min_roi, max_roi = bounds[category]
            return max(min(roi, max_roi), min_roi)
            
        except Exception as e:
            print(f"Error calculating ROI for {upgrade['building']}: {e}")
            return 0
    
    def optimize_upgrade_path(self, available_resources):
        print("\nValidating upgrades...")
        upgrade_path = []
        possible_upgrades = []
        for _, upgrade in self.upgrades.iterrows():
            resource_type = upgrade['resource_type']
            cost = upgrade['cost']
            
            if cost <= available_resources.get(resource_type, 0):
                possible_upgrades.append(upgrade)
                print(f"Found valid {resource_type} upgrade: {upgrade['building']} level {upgrade['level']}")
        
        print(f"\nFound {len(possible_upgrades)} possible upgrades")
        for upgrade in possible_upgrades:
            roi = self.calculate_roi(upgrade)
            building_info = self.buildings[self.buildings['building_name'] == upgrade['building']].iloc[0]
            if roi > -100:
                upgrade_path.append({
                    'building': upgrade['building'],
                    'level': upgrade['level'],
                    'cost': upgrade['cost'],
                    'resource_type': upgrade['resource_type'],
                    'time_hours': upgrade['time_hours'],
                    'roi': roi,
                    'category': building_info['category']
                })
        upgrade_path.sort(key=lambda x: (x['category'], -x['roi']))
        return upgrade_path

    # Fungsi untuk menghitung model time management build
    def calculate_build_time(self, upgrade_path):
        """Calculate total build time with multiple builders"""
        if not upgrade_path:
            return 0
        times = [u['time_hours'] for u in upgrade_path]
        builder_queues = [0] * self.builders
        for time in sorted(times, reverse=True):
            min_queue = min(builder_queues)
            min_index = builder_queues.index(min_queue)
            builder_queues[min_index] += time
        return max(builder_queues)