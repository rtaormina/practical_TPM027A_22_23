# plotly and dash
from dash import Dash, dcc, html, Input, Output
from jupyter_dash import JupyterDash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# others
from datetime import date

def plot_dashboard(df, sensor_names, stats_to_show=[], show_attacks=False):
    app = JupyterDash(__name__)
    
    app.layout = html.Div([
        html.H4('Sensor readings'),
        dcc.Graph(id="time-series-chart"),
        html.P("Select sensor:"),
        dcc.Dropdown(
            id="sensor",
            options=sensor_names,
            value=sensor_names[0],
            clearable=False,
        ),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=df.index[0],
            max_date_allowed=df.index[-1],
            initial_visible_month=df.index[0],
            end_date=df.index[-1]
        ),
        html.Div(id='output-container-date-picker-range')
    ])

    @app.callback(
        Output("time-series-chart", "figure"), 
        Input("sensor", "value"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"))
    def display_time_series(sensor, start_date, end_date):
        if show_attacks == False:                        
            return px.line(df,  range_x=[start_date,end_date], y= [sensor] + [sensor+f'_{stat}' for stat in stats_to_show])
        else:
            fig = make_subplots(rows=2,cols=1, row_heights=[0.7,0.3], shared_xaxes=True)
            
            fig.add_trace(
                go.Scatter(
                    x=df.loc[start_date:end_date].index.tolist(),  
                    y=df.loc[start_date:end_date][sensor], name=sensor),
                row=1,col=1)
            
            for stat in stats_to_show:
                fig.add_trace(
                    go.Scatter(
                        x=df.loc[start_date:end_date].index.tolist(),  
                        y=df.loc[start_date:end_date][sensor+f'_{stat}'], name=sensor+f'_{stat}'),
                    row=1,col=1)
            
            fig.add_trace(
                go.Scatter(
                    x=df.loc[start_date:end_date].index.tolist(),  
                    y=df.loc[start_date:end_date]['ATT_FLAG'], name='attack trace'),
                row=2,col=1)            
        return fig
    return app
