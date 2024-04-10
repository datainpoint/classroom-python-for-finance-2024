from dash import html, dcc, Output, Input, Dash
import sqlite3
from datetime import datetime

update_frequency = 200
figure = dict(data=[{'x': [], 'y': []}], 
              layout=dict(xaxis=dict(autorange=True), yaxis=dict(autorange=True)))
app = Dash()
app.layout = html.Div([
    dcc.Graph(id='graph', figure=figure),
    dcc.Interval(id="interval")]
)

@app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
def update_data(n_intervals):
    conn = sqlite3.connect("agg_trade.db")
    cursor = conn.cursor()
    sql_statement = """
    SELECT *
      FROM btcusdt
     ORDER BY trade_time DESC
     LIMIT 1;
    """
    list_of_tuples = cursor.execute(sql_statement).fetchall()
    latest_trade_time = list_of_tuples[0][1]
    latest_trade_time_dt = datetime.fromtimestamp(latest_trade_time / 1000)
    latest_price = list_of_tuples[0][2]
    # tuple is (dict of new data, target trace index, number of points to keep)
    dict_to_return = {
        "x": [[latest_trade_time_dt]],
        "y": [[latest_price]]
    }
    return (dict_to_return), [0], 100

if __name__ == "__main__":
    app.run_server(debug=True)