import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html

df = pd.read_csv('../datasets/input/stage.csv')
df_loc = df[['latitude', 'longitude', 'state', 'n_killed', 'n_injured', 'date', 'notes']]
df_loc.dropna(inplace=True)

app = dash.Dash(__name__)

# we should distinguish between the cases where there are no victims, only injured, or killed
colors = []
for killed, injured in zip(df_loc['n_killed'], df_loc['n_injured']):
    if killed == 0 and injured == 0:
        colors.append('#43C13E')  
    elif killed == 0 and injured > 0:
        colors.append('#3e43c1')   
    else:
        colors.append('#C13E43') 

fig = go.Figure(go.Scattermapbox(
    lat=df_loc['latitude'],
    lon=df_loc['longitude'],
    mode='markers',
    marker=go.scattermapbox.Marker(size=9, color=colors),
    text=[f"<br>{note}<br> <br>State: {state}<br>Killed:{killed}<br>Injured: {injured}<br>Date: {date}"
          for note, state, killed, injured, date in zip(df_loc['notes'], df_loc['state'], df_loc['n_killed'], df_loc['n_injured'], df_loc['date'])]
))

# fullscreen map 
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, mapbox_style="carto-positron", showlegend=False)

# dash app layout
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig, config={'scrollZoom': True}, style={'height': '100vh'}),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8051)