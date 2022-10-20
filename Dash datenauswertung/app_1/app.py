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
# print(data["zeit"])
# data = pd.read_csv("avocado.csv")
# print(type(data))
# data = data.query("type == 'conventional' and region == 'Albany'")
data["zeit"] = pd.to_datetime(data["zeit"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)
# print(data)

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            children="Tankstellen Anal",
        ),
        html.P(
            children="Analyze the behavior of avocado prices"
                     " and the number of avocados sold in the US"
                     " between 2015 and 2018",
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["zeit"],
                        "y": data["diesel"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Price of Diesel"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["zeit"],
                        "y": data["e5"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Price of E 5"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["zeit"],
                        "y": data["e10"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Price of E 10"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
    # print(type(data))
    print("Start")
