# scripts/data_gen.py

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Create output folder
os.makedirs("../data", exist_ok=True)

# --------------------------
# Dataset 1: Multi-City Traffic Network Data
cities = {
    'Amsterdam': {'lat': 52.3676, 'lon': 4.9041, 'zones': ['City Center', 'Amsterdam Noord', 'Zuidoost', 'West', 'Nieuw-West']},
    'New York': {'lat': 40.7128, 'lon': -74.0060, 'zones': ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']},
    'London': {'lat': 51.5074, 'lon': -0.1278, 'zones': ['Central London', 'North London', 'South London', 'East London', 'West London']},
    'Kuala Lumpur': {'lat': 3.1390, 'lon': 101.6869, 'zones': ['KLCC', 'Chow Kit', 'Bangsar', 'Mont Kiara', 'Petaling Jaya']}
}

# Generate traffic network data with coordinates
network_data = []
current_time = datetime.now()

for city, info in cities.items():
    for i, zone in enumerate(info['zones']):
        # Create realistic coordinates around city center
        lat_offset = np.random.normal(0, 0.05)
        lon_offset = np.random.normal(0, 0.05)
        
        # Generate traffic conditions (mimicking the color coding in the reference)
        traffic_condition = np.random.choice(['Good', 'Moderate', 'Congested'], p=[0.4, 0.4, 0.2])
        speed_mapping = {'Good': (45, 65), 'Moderate': (25, 45), 'Congested': (5, 25)}
        min_speed, max_speed = speed_mapping[traffic_condition]
        
        network_data.append({
            'City': city,
            'Zone': zone,
            'Latitude': info['lat'] + lat_offset,
            'Longitude': info['lon'] + lon_offset,
            'Traffic_Condition': traffic_condition,
            'Current_Speed': np.random.uniform(min_speed, max_speed),
            'Volume': np.random.randint(500, 3000),
            'Timestamp': current_time,
            'Route_Density': np.random.uniform(0.3, 1.0)
        })

df_network = pd.DataFrame(network_data)
df_network.to_csv("../data/traffic_network_data.csv", index=False)

# --------------------------
# Dataset 2: Time Series Traffic Flow Data
time_series = pd.date_range(start='2025-07-08 00:00', periods=24, freq='H')
flow_data = []

for city in cities.keys():
    for hour in time_series:
        # Simulate rush hour patterns
        hour_of_day = hour.hour
        if 7 <= hour_of_day <= 9 or 17 <= hour_of_day <= 19:
            congestion_factor = np.random.uniform(0.6, 0.9)  # Higher congestion during rush
            avg_speed = np.random.uniform(15, 35)
        elif 22 <= hour_of_day or hour_of_day <= 5:
            congestion_factor = np.random.uniform(0.1, 0.3)  # Low congestion at night
            avg_speed = np.random.uniform(50, 70)
        else:
            congestion_factor = np.random.uniform(0.3, 0.6)  # Normal traffic
            avg_speed = np.random.uniform(35, 55)
        
        flow_data.append({
            'City': city,
            'Timestamp': hour,
            'Congestion_Level': congestion_factor,
            'Average_Speed': avg_speed,
            'Traffic_Volume': np.random.randint(800, 4000),
            'Incidents': np.random.poisson(1) if congestion_factor > 0.7 else 0
        })

df_flow = pd.DataFrame(flow_data)
df_flow.to_csv("../data/traffic_flow_timeseries.csv", index=False)

# --------------------------
# Dataset 3: Route Performance Data
route_data = []
route_types = ['Highway', 'Main Road', 'Secondary Road', 'Local Street']

for city in cities.keys():
    for route_type in route_types:
        for i in range(5):  # 5 routes per type per city
            # Performance varies by route type
            if route_type == 'Highway':
                base_speed = np.random.uniform(60, 80)
                efficiency = np.random.uniform(0.7, 0.95)
            elif route_type == 'Main Road':
                base_speed = np.random.uniform(30, 50)
                efficiency = np.random.uniform(0.6, 0.85)
            elif route_type == 'Secondary Road':
                base_speed = np.random.uniform(20, 40)
                efficiency = np.random.uniform(0.5, 0.75)
            else:  # Local Street
                base_speed = np.random.uniform(15, 30)
                efficiency = np.random.uniform(0.4, 0.7)
            
            route_data.append({
                'City': city,
                'Route_Type': route_type,
                'Route_ID': f"{city}_{route_type}_{i+1}",
                'Average_Speed': base_speed + np.random.normal(0, 5),
                'Efficiency_Score': efficiency,
                'Daily_Volume': np.random.randint(1000, 8000),
                'Travel_Time_Index': np.random.uniform(1.0, 2.5)
            })

df_routes = pd.DataFrame(route_data)
df_routes.to_csv("../data/route_performance.csv", index=False)

print("✅ Enhanced traffic data files generated in /data/")
print(f"   - Generated {len(df_network)} network points across {len(cities)} cities")
print(f"   - Generated {len(df_flow)} time series records")
print(f"   - Generated {len(df_routes)} route performance records")
