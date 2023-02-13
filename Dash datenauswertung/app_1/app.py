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
            f'SELECT zeit,avg(diesel),avg(e10),avg(e5) FROM `Tankdaten`.`Data` group by zeit order by zeit desc ;')
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
            children="Tankstellen Analyse",
        ),
        html.P(
            children="Zeigt die Mittelwertdaten der Tankpreiße von ganz Deutschland",
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
