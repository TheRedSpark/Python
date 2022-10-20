import dash
from dash import dcc
from dash import html
import pandas as pd
import mysql.connector
from package import variables as v

ort = "home"
database = "Tankdaten"


def data_getter():
    with mysql.connector.connect(
            host=v.host(ort),
            user=v.user(ort),
            passwd=v.passwd(ort),
            database=v.database(database),
            auth_plugin='mysql_native_password') as mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute(
            f'SELECT zeit,diesel,e10,e5 FROM `Tankdaten`.`Data` WHERE id ="e3ab6579-0b05-492e-8e74-c46e47923e71" ')
        df = pd.DataFrame(my_cursor.fetchall(), columns=['zeit', 'diesel', 'e10', 'e5'])
        # print(df)
        # print(type(df))
        return df


data = data_getter()

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["zeit"],
                                    "y": data["e10"],
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}"
                                    "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Benzinpreise",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    "tickprefix": "$",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["zeit"],
                                    "y": data["diesel"],
                                    "type": "lines",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Dieselpreise",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {"fixedrange": True},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
