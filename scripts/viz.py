# scripts/viz.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Read Enhanced Data
df_network = pd.read_csv("../data/traffic_network_data.csv")
df_flow = pd.read_csv("../data/traffic_flow_timeseries.csv")
df_routes = pd.read_csv("../data/route_performance.csv")

# Convert timestamp columns
df_flow['Timestamp'] = pd.to_datetime(df_flow['Timestamp'])

# Color mapping for traffic conditions (matching reference image)
color_map = {
    'Good': '#00FF00',      # Green
    'Moderate': '#FFA500',  # Orange  
    'Congested': '#FF0000'  # Red
}

# --------------------------
# Create Multi-City Traffic Dashboard
# --------------------------

# 1. Main Traffic Network Map (inspired by reference multi-city view)
fig_map = go.Figure()

for city in df_network['City'].unique():
    city_data = df_network[df_network['City'] == city]
    
    fig_map.add_trace(go.Scattermapbox(
        lat=city_data['Latitude'],
        lon=city_data['Longitude'],
        mode='markers',
        marker=dict(
            size=city_data['Volume']/50,  # Size based on traffic volume
            color=[color_map[condition] for condition in city_data['Traffic_Condition']],
            sizemode='diameter'
        ),
        text=[f"<b>{row['City']} - {row['Zone']}</b><br>" +
              f"Condition: {row['Traffic_Condition']}<br>" +
              f"Speed: {row['Current_Speed']:.1f} km/h<br>" +
              f"Volume: {row['Volume']}" 
              for _, row in city_data.iterrows()],
        hovertemplate='%{text}<extra></extra>',
        name=city,
        showlegend=True
    ))

fig_map.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=30, lon=0),  # Center between all cities
        zoom=1
    ),
    title=dict(
        text="<b>Global Traffic Network Monitoring Dashboard</b>",
        font=dict(size=24, family='Arial', color='black'),
        x=0.5
    ),
    height=500,
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    )
)

# --------------------------
# 2. Traffic Flow Time Series Analysis
fig_timeseries = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Traffic Volume Over Time', 'Average Speed Trends', 
                   'Congestion Levels', 'Incident Reports'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# Traffic Volume
for city in df_flow['City'].unique():
    city_flow = df_flow[df_flow['City'] == city]
    fig_timeseries.add_trace(
        go.Scatter(x=city_flow['Timestamp'], y=city_flow['Traffic_Volume'],
                  mode='lines', name=f'{city} Volume', line=dict(width=3)),
        row=1, col=1
    )

# Average Speed
for city in df_flow['City'].unique():
    city_flow = df_flow[df_flow['City'] == city]
    fig_timeseries.add_trace(
        go.Scatter(x=city_flow['Timestamp'], y=city_flow['Average_Speed'],
                  mode='lines', name=f'{city} Speed', line=dict(width=3)),
        row=1, col=2
    )

# Congestion Levels (Area Chart)
for city in df_flow['City'].unique():
    city_flow = df_flow[df_flow['City'] == city]
    fig_timeseries.add_trace(
        go.Scatter(x=city_flow['Timestamp'], y=city_flow['Congestion_Level'],
                  mode='lines', fill='tonexty' if city != df_flow['City'].unique()[0] else 'tozeroy',
                  name=f'{city} Congestion', line=dict(width=2)),
        row=2, col=1
    )

# Incidents
for city in df_flow['City'].unique():
    city_flow = df_flow[df_flow['City'] == city]
    fig_timeseries.add_trace(
        go.Bar(x=city_flow['Timestamp'], y=city_flow['Incidents'],
               name=f'{city} Incidents', opacity=0.7),
        row=2, col=2
    )

fig_timeseries.update_layout(
    height=600,
    title_text="<b>24-Hour Traffic Analytics Dashboard</b>",
    title_font=dict(size=20, family='Arial', color='black'),
    showlegend=False
)

# Update axes labels
fig_timeseries.update_xaxes(title_text="Time", row=2, col=1)
fig_timeseries.update_xaxes(title_text="Time", row=2, col=2)
fig_timeseries.update_yaxes(title_text="Vehicles", row=1, col=1)
fig_timeseries.update_yaxes(title_text="Speed (km/h)", row=1, col=2)
fig_timeseries.update_yaxes(title_text="Congestion Level", row=2, col=1)
fig_timeseries.update_yaxes(title_text="Incidents", row=2, col=2)

# --------------------------
# 3. Route Performance Analysis (inspired by traffic condition colors)
fig_performance = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Route Efficiency by Type', 'Speed Distribution Analysis'),
    specs=[[{"type": "xy"}, {"type": "xy"}]]
)

# Route efficiency box plot
for route_type in df_routes['Route_Type'].unique():
    route_data = df_routes[df_routes['Route_Type'] == route_type]
    fig_performance.add_trace(
        go.Box(y=route_data['Efficiency_Score'], name=route_type,
               boxpoints='outliers', jitter=0.3, pointpos=-1.8),
        row=1, col=1
    )

# Speed distribution histogram
colors = px.colors.qualitative.Set3
for i, city in enumerate(df_routes['City'].unique()):
    city_routes = df_routes[df_routes['City'] == city]
    fig_performance.add_trace(
        go.Histogram(x=city_routes['Average_Speed'], name=city,
                    opacity=0.7, nbinsx=15,
                    marker_color=colors[i % len(colors)]),
        row=1, col=2
    )

fig_performance.update_layout(
    height=400,
    title_text="<b>Route Performance & Speed Distribution Analysis</b>",
    title_font=dict(size=20, family='Arial', color='black'),
    barmode='overlay'
)

fig_performance.update_xaxes(title_text="Route Type", row=1, col=1)
fig_performance.update_xaxes(title_text="Average Speed (km/h)", row=1, col=2)
fig_performance.update_yaxes(title_text="Efficiency Score", row=1, col=1)
fig_performance.update_yaxes(title_text="Frequency", row=1, col=2)

# --------------------------
# 4. Traffic Condition Summary (Pie Charts)
condition_summary = df_network['Traffic_Condition'].value_counts()

fig_summary = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "domain"}, {"type": "xy"}]],
    subplot_titles=('Traffic Condition Distribution', 'City Performance Comparison')
)

# Pie chart for traffic conditions
fig_summary.add_trace(
    go.Pie(labels=condition_summary.index, values=condition_summary.values,
           marker_colors=[color_map[condition] for condition in condition_summary.index],
           name="Traffic Conditions"),
    row=1, col=1
)

# City performance bar chart
city_performance = df_network.groupby('City').agg({
    'Current_Speed': 'mean',
    'Volume': 'sum'
}).reset_index()

fig_summary.add_trace(
    go.Bar(x=city_performance['City'], y=city_performance['Current_Speed'],
           name='Avg Speed', marker_color='lightblue', yaxis='y'),
    row=1, col=2
)

fig_summary.add_trace(
    go.Scatter(x=city_performance['City'], y=city_performance['Volume']/100,
               mode='markers+lines', name='Volume (x100)', 
               marker=dict(size=12, color='red'), yaxis='y2'),
    row=1, col=2
)

fig_summary.update_layout(
    height=400,
    title_text="<b>Traffic Network Summary & City Comparison</b>",
    title_font=dict(size=20, family='Arial', color='black'),
    yaxis2=dict(overlaying='y', side='right', title='Traffic Volume'),
)

fig_summary.update_xaxes(title_text="City", row=1, col=2)
fig_summary.update_yaxes(title_text="Average Speed (km/h)", row=1, col=2)

# --------------------------
# Combine into Master Dashboard
master_dashboard = make_subplots(
    rows=4, cols=1,
    row_heights=[0.35, 0.3, 0.2, 0.15],
    subplot_titles=('Global Traffic Network Map', 
                   '24-Hour Traffic Analytics',
                   'Route Performance Analysis', 
                   'Network Summary'),
    specs=[[{"type": "mapbox"}],
           [{"type": "xy"}],
           [{"type": "xy"}], 
           [{"type": "xy"}]],
    vertical_spacing=0.05
)

# Note: Due to complexity, we'll create separate exports
# Create outputs directory
os.makedirs("../outputs", exist_ok=True)

# Export individual charts and main dashboard
fig_map.write_html("../outputs/traffic_map.html")
fig_timeseries.write_html("../outputs/timeseries_analysis.html")
fig_performance.write_html("../outputs/performance_analysis.html")
fig_summary.write_html("../outputs/summary_dashboard.html")

# Create the main comprehensive dashboard
main_dashboard = go.Figure()

# Add a text annotation explaining the dashboard
main_dashboard.add_annotation(
    text="<b style='font-size:28px'>Global Traffic Monitoring Operations Center</b><br><br>" +
         "🟢 Good Traffic Flow &nbsp;&nbsp;&nbsp; 🟠 Moderate Congestion &nbsp;&nbsp;&nbsp; 🔴 Heavy Congestion<br><br>" +
         "<i>Real-time monitoring across Amsterdam, New York, London, and Kuala Lumpur</i><br>" +
         "Dashboard includes: Network mapping, time-series analysis, route performance, and summary statistics",
    x=0.5, y=0.5,
    xref="paper", yref="paper",
    showarrow=False,
    font=dict(size=16, family='Arial'),
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="black",
    borderwidth=2
)

main_dashboard.update_layout(
    title=dict(
        text="<b>Multi-City Traffic Dashboard - Operations Center</b>",
        font=dict(size=24, family='Arial', color='black'),
        x=0.5
    ),
    height=400,
    plot_bgcolor='white'
)

main_dashboard.write_html("../outputs/dashboard.html")

# Generate screenshot using the map (most representative)
fig_map.write_image("../outputs/screenshot.png", width=1200, height=800, scale=2)

print("✅ Comprehensive Traffic Dashboard generated successfully!")
print("   📊 Main dashboard: /outputs/dashboard.html")
print("   🗺️  Traffic map: /outputs/traffic_map.html") 
print("   📈 Time series: /outputs/timeseries_analysis.html")
print("   ⚡ Performance: /outputs/performance_analysis.html")
print("   📋 Summary: /outputs/summary_dashboard.html")
print("   📸 Screenshot: /outputs/screenshot.png")
