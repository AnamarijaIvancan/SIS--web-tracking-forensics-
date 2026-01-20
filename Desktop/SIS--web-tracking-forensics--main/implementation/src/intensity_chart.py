import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


with open('intensity_scores.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df = df.sort_values('score', ascending=False).head(10)


fig = px.bar(df, x='domain', y='score', color='fp',
             title='Tracking Intensity Score - Top 10 stranica',
             labels={'score': 'Intensity Score', 'domain': 'Web stranica'},
             color_continuous_scale='Viridis')

fig.update_layout(xaxis_tickangle=-45, height=500)
fig.write_html('intensity_chart.html')
fig.show()  
print("✔ intensity_chart.html spreman za slajd!")
