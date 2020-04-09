from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
import dash_daq as daq
import plotly.graph_objects as go
from datetime import datetime
from app import app
import pandas as pd
from data.map import get_map
from data.data import COVID19India
from data.inshorts_news import InshortsNews
from data.data_processing import get_daily_data, get_interval_data, get_state_daily

inshorts = InshortsNews()
covidin = COVID19India()from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
import dash_daq as daq
import plotly.graph_objects as go
from datetime import datetime
from app import app
import pandas as pd
from data.map import get_map
from data.data import COVID19India
from data.inshorts_news import InshortsNews
from data.data_processing import get_daily_data, get_interval_data, get_state_daily

inshorts = InshortsNews()
covidin = COVID19India()

# bar_graph1 = dcc.Graph(
#     id='bar-graph1',
#     figure={
#         'data': [{'x': df1['date'], 'y': df1['confirmed'] - df1["recovered"] - df1["deaths"],
#                   'type': 'bar', 'name': 'Active Cases'},
#                  {'x': df1['date'], 'y': df1["recovered"], 'type': 'bar', "marker": {'color': "green"},
#                   'name': 'Recovered Case'},
#                  {'x': df1['date'], 'y': df1["deaths"], 'type': 'bar', 'name': 'Deaths',
#                   "marker": {'color': "red"}, }
#                  ],
#         'layout': {
#             'title': f'Covid19 India Cases by Day',
#             'barmode': 'stack',
#             'height': 700,
#             'xaxis': x_axis,
#             'yaxis': y_axis,
#             'plot_bgcolor': colors['background2'],
#             'paper_bgcolor': colors['background'],
#             'font': {
#                 'color': colors['text'],
#                 'size': 18
#             },
#             # 'annotations': annotations
#         }
#     }
# )