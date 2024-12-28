from turtle import title
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