# file app.py

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go

es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)

xs = list(range(30))
ys = [10000 * 1.07**i for i in xs]

fig = go.Figure(data=go.Scatter(x=xs, y=ys))
fig.update_layout(xaxis_title='Years', yaxis_title='$')

app.layout = html.Div(children=[
    html.H1(children='Assets'),
    dcc.Graph(figure=fig)])

if __name__ == '__main__':
    app.run_server(debug=True)