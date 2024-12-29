import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


data = pd.read_csv('dynamic_pricing.csv')
print(data.head())
print(data.describe())

data['Expected_Ride_Duration'] = pd.to_numeric(data['Expected_Ride_Duration'], errors='coerce')
data['Historical_Cost_of_Ride'] = pd.to_numeric(data['Historical_Cost_of_Ride'], errors='coerce')

data = data.dropna()

fig = px.scatter(
    data, x='Expected_Ride_Duration',
    y='Historical_Cost_of_Ride',
    title='Expected Ride Duration vs. Historical Cost of Ride',
    trendline='ols'
)
fig.show()

fig = px.box(data, x='Vehicle_Type',
             y='Historical_Cost_of_Ride',
             title='Historical Cost of Ride Distribution by Vehicle Type')
fig.show()

numeric_data = data.select_dtypes(include=['float64', 'int64'])
corr_matrix = numeric_data.corr()
fig = go.Figure(data=go.Heatmap(z=corr_matrix.values,
                                x=corr_matrix.columns,
                                y=corr_matrix.columns,
                                colorscale='Viridis'))
fig.update_layout(title='Correlation Matrix')
fig.show()

high_demand_percentile = 75
low_demand_percentile = 25
data['demand_multiplier'] = np.where(data['Number_of_Riders'] > np.percentile(data['Number_of_Riders'], high_demand_percentile), 
data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], high_demand_percentile),
data['Number_of_Riders'] / np.percentile(data['Number_of_Riders'], low_demand_percentile))

high_supply_percentile = 75
low_supply_percentile = 25
data['supply_multiplier'] = np.where(data['Number_of_Drivers'] > np.percentile(data['Number_of_Drivers'], low_supply_percentile),
np.percentile(data['Number_of_Drivers'], high_supply_percentile) / data['Number_of_Drivers'],
np.percentile(data['Number_of_Drivers'], low_supply_percentile) / data['Number_of_Drivers'])

demand_threshold_high = 1.2
demand_threshold_low = 0.8
supply_threshold_high = 0.8
supply_threshold_low = 1.8

data['adjusted_ride_cost'] = data['Historical_Cost_of_Ride'] * (
    np.maximum(data['demand_multiplier'], demand_threshold_low) * 
    np.maximum(data['supply_multiplier'], supply_threshold_high)
)

data['profit_percentage'] = ((data['adjusted_ride_cost'] - data['Historical_Cost_of_Ride']) / data['Historical_Cost_of_Ride']) * 100
profitable_rides = data[data['profit_percentage'] > 0]
loss_rides = data[data['profit_percentage'] < 0]

profitable_count = len(profitable_rides)
loss_count = len(loss_rides)

labels = ['Profitable_Rides', 'Loss Rides']
values = [profitable_count, loss_count]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
fig.update_layout(title='Profitability of Rides (Dynamic Pricing vs. Historical Pricing)')
fig.show()
