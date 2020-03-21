from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_daq as daq
from datetime import datetime
from data.data import COVID19India

covidin = COVID19India()
df = pd.read_csv('data/21.03.2020_moh_india.csv')
colors = {
    'background': 'white',
    'background2': 'black',
    'text': '#000080'
}

y_axis = {
    'title': 'Price',
    'showspikes': True,
    'spikedash': 'dot',
    'spikemode': 'across',
    'spikesnap': 'cursor',
}

x_axis = {
    'title': 'Time',
    'showspikes': True,
    'spikedash': 'dot',
    'spikemode': 'across',
    'spikesnap': 'cursor',
}

data_display = """
| **Name of State / UT** | **Total Confirmed cases (Indian National)** | **Total Confirmed cases ( Foreign National )** | |**Cured/Discharged/Migrated** |  | **Death** |
|:---------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
"""
# df = df.sort_values('Total Confirmed cases (Indian National)', ascending=False)
for value in df.values:
    v = f"""|{value[0]}|{value[1]}|{value[2]}||{value[3]}||{value[4]}|\n"""
    data_display += v

data_ranger = dcc.DatePickerRange(
    id='date-input',
    stay_open_on_select=False,
    min_date_allowed=datetime(2020, 1, 30),
    max_date_allowed=datetime.now(),
    initial_visible_month=datetime.now(),
    start_date=datetime(2020, 3, 1),
    end_date=datetime.now(),
    number_of_months_shown=2,
    month_format='MMMM,YYYY',
    display_format='YYYY-MM-DD',
    style={
        'color': '#11ff3b',
        'font-size': '18px',
        'margin': 0,
        'padding': '8px',
        'background': 'yellow',
        'display': 'inline-block'
    }
)

app.layout = html.Div([html.H1("COVID19 India Tracker",
                               style={
                                   'textAlign': 'center',
                                   "background": "yellow"}),
                       html.Div([
                                 html.Span("Total Active Cases: "),
                                 html.Div(id='active-display', style={'display': 'inline-block'}),
                                html.Span("Total Recovered Cases: "),
                                html.Div(id='recovered-display', style={'display': 'inline-block'}),
                                html.Span("Total Deaths: "),
                                 html.Div(id='death-display', style={'display': 'inline-block'}),
                                html.Span("Total affected States and UTs: "),
                                 html.Div(id='counts-display', style={'display': 'inline-block'})
                                 ], className="row ",
                                style={
                                    'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'white',
                                       'display': 'inline-block',
                                       }),
                       # html.Hr(style={'border': '2px solid black'}),
                       html.Div(['Data Range',
                                 data_ranger], style={'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'white',
                                       'display': 'none'}),
                       html.Div(id='graph-input'),
                       html.H1(id='graph-output'),
                       html.Div(children=[html.H2(children="Data",
                                                  style={
                                                      'textAlign': 'center',
                                                      "background": "yellow"}),
                                          ]),
                       html.Div(id='intermediate-value', style={'display': 'none'}),
                        html.Div(children=[dcc.Markdown(  # markdown
                                                   data_display)], style={
                                                   'textAlign': 'center',
                                                   "background": "#CCFFFF",
                                                   "padding": "70px 0",
                        }),
                        html.Div(children=[dcc.Markdown(  # markdown
                           " Data Resources: [MInistry of Health and Family Welfare, GoI](https://www.mohfw.gov.in/) and [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) ")], style={
                           'textAlign': 'center',
                           "background": "yellow"}),
                       html.Div(children=[dcc.Markdown(  # markdown
                           " © 2020 [DCAICHARA](https://github.com/dc-aichara)  All Rights Reserved.")], style={
                           'textAlign': 'center',
                           "background": "yellow"}),
                       html.Div(id='dummy-id'),

                       ], style={
    "background": "#000080"}
                      )


@app.callback(Output('intermediate-value', 'children'),
              [Input('dummy-id', '')])
def get_data(_):
    df = covidin.jhu_india_data(save=False)
    return df.to_json(date_format='iso', orient='split')


@app.callback(Output(component_id='graph-output', component_property='children'),
              [Input('intermediate-value', 'children'),
               Input('date-input', 'start_date'),
               Input('date-input', 'end_date')])
def render_graph(data, start_date, end_date):
    try:
        df = pd.read_json(data, orient='split')
    except:
        df = pd.read_csv('data/20-03-2020_jhu_india.csv')
    df['date'] = pd.to_datetime(df['date'])
    data = df[(df.date >= start_date) & (df.date <= end_date)]
    return dcc.Graph(
        id='graph-1',
        figure={
            'data': [
                {'x': data['date'], 'y': data["confimred"], 'type': 'line', 'name': 'Confirmed Cases',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'cross-open'}},
                {'x': data['date'], 'y': data["recovered"], 'type': 'line', 'name': 'Recovered Case',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'star-open'}},
                {'x': data['date'], 'y': data["deaths"], 'type': 'line', 'name': 'Deaths',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'x-open'}},
            ],
            'layout': {
                'title': 'Covid19 India Cases',
                'height': 700,
                'xaxis': x_axis,
                'yaxis': y_axis,
                'plot_bgcolor': colors['background2'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text'],
                    'size': 18
                }
            }
        }
    )


@app.callback([Output('active-display', 'children'),
                Output('recovered-display', 'children'),
                Output('death-display', 'children'),
               Output('counts-display', 'children')
               ],
              [Input('dummy-id', '')])
def display_cases(_):
    df = pd.read_csv('data/21.03.2020_moh_india.csv')
    value = df.values[-1][1:].tolist()
    active_case = value[0] + value[1] - value[2] - value[3]
    recovered_case = value[2]
    deaths = value[-1]
    counts = len(df) - 1
    a = daq.LEDDisplay(
                            label={'label': "", 'style': {'font-size': "14px",
                                                             'color': 'green',
                                                             'font-family': 'sans-serif',
                                                             'background': 'black',
                                                             'padding': '2px'
                                                        }
                                   },
                            labelPosition='left',
                            value=str(active_case),
                            backgroundColor='black',
                            size=18,
                            # family='sans-serif',
                            style={'display': 'inline-block',
                                   },
                        )
    b = daq.LEDDisplay(
        label={'label': "", 'style': {'font-size': "14px",
                                      'color': 'green',
                                      'font-family': 'sans-serif',
                                      'background': 'black',
                                      'padding': '2px'
                                      }
               },
        labelPosition='left',
        value=str(recovered_case),
        backgroundColor='green',
        size=18,
        # family='sans-serif',
        style={'display': 'inline-block',
               },
    )
    c = daq.LEDDisplay(
        label={'label': "", 'style': {'font-size': "14px",
                                      'color': 'green',
                                      'font-family': 'sans-serif',
                                      'background': 'black',
                                      'padding': '2px'
                                      }
               },
        labelPosition='left',
        value=str(deaths),
        backgroundColor='red',
        size=18,
        # family='sans-serif',
        style={'display': 'inline-block',
               },
    )
    d = daq.LEDDisplay(
        label={'label': "", 'style': {'font-size': "14px",
                                      'color': 'green',
                                      'font-family': 'sans-serif',
                                      'background': 'black',
                                      'padding': '2px'
                                      }
               },
        labelPosition='left',
        value=str(counts),
        backgroundColor='gray',
        size=18,
        # family='sans-serif',
        style={'display': 'inline-block',
               },
    )
    return [a, b, c, d]


if __name__ == '__main__':
    app.run_server(debug=True)
