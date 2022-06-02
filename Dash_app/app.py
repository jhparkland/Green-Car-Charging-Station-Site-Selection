from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

server = Flask(__name__)
app = Dash(__name__,
           server=server)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Dash에서 h1부분'),

    html.Div(children='''
        걍 잡것 씨부리기.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8050, debug=True)
    app.run_server()