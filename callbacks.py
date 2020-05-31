from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
from app import app
import pandas as pd
from map.scatter_map import scatter_mapbox
from data.data import COVID19India
from data.inshorts_news import InshortsNews
from data.data_processing import get_daily_data, get_interval_data
from styles import colors, y_axis, x_axis, x_axis_bar, y_axis_h, x_axis_h, y_axis_p, x_axis_p, y_axis_t, x_axis_t, \
    y_axis_t2, area_style

inshorts = InshortsNews()
covidin = COVID19India()

try:
    df = covidin.moh_data(save=True)
except:
    df = pd.read_csv('data/archieve_data/2020.04.22_moh_india.csv')

# Create map
india_map = scatter_mapbox(data=df)

df2 = covidin.change_cal()

data_display = """
| **Name of State / UT** | **Total Confirmed cases** |**Cured/Discharged/Migrated** | **Death** |
|:---------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
"""
# print(df)
for v1, v2 in zip(df.values, df2.values):
    a = v1[0]
    b = v1[1] if v2[1] == 0 else f"{v1[1]} (**+{v2[1]}**)"
    c = v1[2] if v2[2] == 0 else f"{v1[2]} (**+{v2[2]}**)"
    d = v1[3] if v2[3] == 0 else f"{v1[3]} (**+{v2[3]}**)"
    # e = v1[4] if v2[4] == 0 else f"{v1[4]} (**+{v2[4]}**)"
    v = f"""|{a}|{b}|{c}|{d}|\n"""
    data_display += v

data_head = html.Div(id="state-data", children=[dcc.Markdown(  # markdown
    f"# COVID19 STATEWISE STATUS \n(As on :  {covidin.last_update()} Source: MoHFW | GoI)")], style={
    'textAlign': 'center',
    "background": "yellow",
})

# Recover and Death rate on previous day
c = df.values[0][1:] - df2.values[0][1:]
c1 = c[1:] / c[0]  # On total
c2 = c[1:] / c[1:].sum()  # On total outcomes (Recovered + Deaths)

# News on corona virus
try:
    news_data = inshorts.get_news()
    news_data = news_data.drop_duplicates()
    news_data = news_data[:30]
except:
    news_data = pd.DataFrame(data=["", ""], columns=['headings', 'news'])

news = []
i = 0
for v in news_data.values:
    if 'corona' in v[1] or 'covid' in v[1]:
        N = html.Div(className=f"news-{i}", children=[html.H2(v[0],
                                                              style={"textAlign": "left",
                                                                     "color": "rgb(158, 239, 32)",
                                                                     "margin-top": 0,
                                                                     "margin-bottom": 0}),
                                                      html.H6(v[1], id='newsline',
                                                              style={"textAlign": "left", 'size': 14,
                                                                     "color": '#3992ec'})],
                     style={'display': 'inline-block',
                            "textAlign": "center",
                            }
                     )
        news.append(N)
        i += 1
source = dcc.Markdown(  # markdown
    '#### Source:  [InShorts](https://www.inshorts.com/en/read/)',
    style={'textAlign': 'right', "white-space": "pre", "overflow-x": "scroll"})
news.append(source)

news1 = html.Div(children=news, style={
    "background": "#CCFFFF",
    "textAlign": "center",
    "padding": "10px 0",
})

# Information on corona virus
help_info = """
     # [GOI official Information Portal](https://www.mygov.in/covid-19)
    # [World Health Organization](https://www.who.int/emergencies/diseases/novel-coronavirus-2019)
    # [Ministry of Health and Family Welfare | GOI](https://www.mohfw.gov.in/)
    # [Government Laboratories Approved by ICMR](https://icmr.nic.in/sites/default/files/upload_documents/Final_Government_Laboratories_Testing_2303.pdf)
    """
info = html.Div(children=[dcc.Markdown(  # markdown
    help_info)], style={
    'textAlign': 'left',
    "background": "gray"})

# Cases distribution
t = df.values[0][1:]
t1 = t[1:] / t[0]  # On total
t2 = t[1:] / t[1:].sum()  # On total outcomes (Recovered + Deaths)
ct1 = t1[0] - c1[0]
ct2 = t1[1] - c1[1]
ct3 = t2[0] - c2[0]
ct4 = t2[1] - c2[1]
piev = [t[0], t[0] - t[1] - t[2], t[1], t[2]]
fig = go.Figure(go.Sunburst(
    labels=["Covid19", "Confirmed", "Active", "Recovered", "Deaths", ],
    parents=["", "Covid19", "Confirmed", "Covid19", "Covid19"],
    values=[0] + piev,
    marker=dict(
        # colors=["blue", 'gray', 'orange', 'yellow', 'red'],
        colors=[a / piev[0] * 100 for a in [0] + piev],
        colorscale='RdBu',
        cmid=50
    ),
    hovertemplate='<b> %{label} Cases <br> </b> %{value} (%{color:.2f} %)',
    name='1'
))
fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                  title='Covid19 India: Cases Distribution',
                  height=280,
                  width=410,
                  paper_bgcolor='#eae2e2',
                  font={'size': 16}
                  )
pie = dcc.Graph(id='pie-chart', figure=fig)
analysis1 = html.Div([html.Div(children=
                               [html.Div(className="r-rate", id='rrate',
                                         children=[html.H5("Recover Rate", style={'color': 'green'}),
                                                   html.H5(f"{piev[2] / piev[0]:.2%}"),
                                                   html.Span(f"{ct1:.2%}" + "{}".format("▲" if ct1 > 0 else "▼"),
                                                             style={
                                                                 "color": 'green' if ct1 > 0 else "red"
                                                             }
                                                             )
                                                   ],
                                         style={
                                             "textAlign": "center",
                                             "width": "140px",
                                         }
                                         ),
                                html.Div(className="d-rate", id='drate',
                                         children=[html.H5("Death Rate", style={'color': 'red'}),
                                                   html.H5(f"{piev[3] / piev[0]:.2%}"),
                                                   html.Span(f"{ct2:.2%}" + "{}".format("▲" if ct2 > 0 else "▼"),
                                                             style={
                                                                 "color": 'green' if ct2 < 0 else "red"
                                                             }
                                                             )
                                                   ],
                                         style={
                                             "textAlign": "center",
                                             "width": "140px",
                                         }),
                                html.Span('on total confirm cases')
                                ],
                               className="container-display1", style={'textAlign': 'center',
                                                                      'display': 'inline-block',
                                                                      "verticalAlign": "top",
                                                                      }
                               ),
                      html.Div([pie], style={'textAlign': 'center',
                                             "verticalAlign": "text-top",
                                             'display': 'inline-block'}),
                      html.Div(children=
                               [html.Div(className="r-rate", id='rrate',
                                         children=[html.H5("Recover Rate", style={'color': 'green'}),
                                                   html.H5(f"{piev[2] / (piev[2] + piev[3]):.2%}"),
                                                   html.Span(f"{ct3:.2%}" + "{}".format("▲" if ct3 > 0 else "▼"),
                                                             style={
                                                                 "color": 'green' if ct3 > 0 else "red"
                                                             }
                                                             )
                                                   ],
                                         style={
                                             "textAlign": "center",
                                             "width": "140px",
                                         }
                                         ),
                                html.Div(className="d-rate", id='drate',
                                         children=[html.H5("Death Rate", style={'color': 'red'}),
                                                   html.H5(f"{piev[3] / (piev[2] + piev[3]):.2%}"),
                                                   html.Span(f"{ct4:.2%}" + "{}".format("▲" if ct4 > 0 else "▼"),
                                                             style={
                                                                 "color": 'green' if ct4 < 0 else "red"
                                                             }
                                                             )
                                                   ],
                                         style={
                                             "textAlign": "center",
                                             "width": "140px",
                                         }),
                                html.Span('on total outcomes'),
                                html.Br(),
                                html.Span('(Recover + Death)')
                                ],
                               className="container-display1", style={'textAlign': 'center',
                                                                      'display': 'inline-block',
                                                                      "verticalAlign": "top",
                                                                      }
                               ),
                      ],
                     className="row-pie", style={
        'background': '#eae2e2',
        'textAlign': 'center'})

# Daily tests
tests = covidin.tests()
# tests = tests[tests['totalpositivecases'] != ""]
# tests['totalpositivecases'] = tests['totalpositivecases'].str.replace(',', '')
# tests['positive_rate'] = round(
#     (tests['totalpositivecases'].astype(int) / tests["totalsamplestested"].astype(int)) * 100, 2)
tests['updatetimestamp'] = pd.to_datetime(tests['updatetimestamp'].apply(lambda x: x.split(" ")[0]), dayfirst=True)
# tests = tests[['totalpositivecases', 'totalsamplestested', 'updatetimestamp', 'positive_rate']]
tests = tests.drop_duplicates("updatetimestamp")
test_graph = dcc.Graph(
    id='test-plot',
    figure={
        'data': [
            # {'y': tests['totalpositivecases'], 'x': tests['updatetimestamp'],
            #       'type': 'line', 'name': 'Positive Cases'},
            {'x': tests['updatetimestamp'], 'y': tests['totalsamplestested'],
             'type': 'bar', 'name': 'Total Tests', "marker": {'color': '#100E2F'}},
            # {'y': tests['positive_rate'], 'x': tests['updatetimestamp'],
            #  'type': 'line', 'name': 'Positive Rate', 'yaxis': 'y2'},
        ],
        'layout': {
            'legend': {'x': 0.10, 'y': 0.9},
            'title': f'Covid19 India: Daily Tests',
            'xaxis': x_axis_t,
            'yaxis': y_axis_t,
            # 'yaxis2': y_axis_t2,
            'plot_bgcolor': colors['background2'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text'],
                'size': 13
            },
            "margin": {'b': 50, "t": 50}
        }
    }
)
# District level visualization
dists = covidin.state_district_data()
d_fig = px.sunburst(dists, path=['State_UT', 'District'],
                    values='Confirmed', color='State_UT',
                    hover_data=["Confirmed", "District", 'State_UT']
                    )
d_fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                    title='Covid19 India: Districtwise Cases Distribution',
                    height=700,
                    # width=410,
                    paper_bgcolor='#eae2e2',
                    font={'size': 16}
                    )
d_fig.data[0].update(
    hovertemplate="%{customdata[1]}, %{customdata[2]} <br>Confirmed: %{customdata[0]}"
)
dist_chart = dcc.Graph(id='dist-chart', figure=d_fig)


@app.callback(Output('api-data', 'children'),
              [Input('dummy-id', '')])
def get_data(_):
    try:
        df_api = covidin.timeseries_data()
        df_api['date'] = pd.to_datetime(df_api['date'] + '2020')
        df_api = df_api[df_api['dailyconfirmed'] != ""]
        df_api = df_api[
            ["date", "totalconfirmed", "totalrecovered", "totaldeceased", 'dailyconfirmed', 'dailyrecovered',
             'dailydeceased']]
        df_api.columns = ['date', 'confirmed', 'recovered', 'deaths', 'daily_confirmed', 'daily_recovered',
                          'daily_deaths']
        df_api.to_csv('data/api_india.csv', index=False)
    except:
        df_api = pd.read_csv("data/api_india.csv")

    df_api['date'] = pd.to_datetime(df_api['date'])
    return df_api.to_json(date_format='iso', orient='split')


@app.callback([Output('active-display', 'children'),
               Output('recovered-display', 'children'),
               Output('death-display', 'children'),
               Output('counts-display', 'children'),
               Output('confirm-display', 'children')
               ],
              [Input('dummy-id', '')])
def display_cases(_):
    value = df.values[0][1:].tolist()
    active_case = value[0] - value[1] - value[2]
    recovered_case = value[1]
    deaths = value[-1]
    counts = len(df) - 1
    total = value[0]

    def daq_display(value, clr):
        display = daq.LEDDisplay(
            label={'label': "  ", 'style': {'font-size': "14px",
                                            'color': 'green',
                                            'font-family': 'sans-serif',
                                            'background': 'white',
                                            'padding': '2px',
                                            }
                   },
            labelPosition='left',
            value=str(value),
            backgroundColor=clr,
            size=19,
            style={'display': 'inline-block',
                   },
        )
        return display

    a = daq_display(active_case, 'black')
    b = daq_display(recovered_case, 'green')
    c = daq_display(deaths, 'red')
    d = daq_display(counts, 'gray')
    e = daq_display(total, '#6F727A')

    return [a, b, c, d, e]


@app.callback(Output(component_id='graph-output', component_property='children'),
              [Input('api-data', 'children'),
               Input('all-tabs-inline', 'value')])
def render_graph(data, tab):
    try:
        df_daily = pd.read_json(data, orient='split')
    except:
        df_daily = pd.read_csv('data/api_india.csv')
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    df1 = get_daily_data(df_daily)
    data = df1[df1.date > "2020-02-29"]
    df_itvl = get_interval_data(days=7, cases=df1, cols=None)
    state_data = html.Div(className='India-data',
                          children=[
                              html.Div(children=[dcc.Markdown(data_display)], className='data-table',
                                       style={'display': 'inline-block'}),
                              html.Div(children=[dcc.Graph(figure=india_map)], className='India-map',
                                       style={'display': 'inline-block', 'textAlign': 'center'})
                          ]
                          )
    dates_index = [6, 13, 20, 27, 34, 41, 48, 55, 62, 69, 76, 83, 90]
    annotations = [{
        'x': pd.to_datetime(data['date'].values[i]),
        'y': data['confirmed'].values[i],
        'showarrow': True,
        'text': f"Week{j + 1}: {data['confirmed'].values[i]}",
        "font": {"color": 'red', 'size': 12},
        'xref': 'x',
        'yref': 'y',
    }
        for j, i in enumerate(dates_index)]

    if tab == 'tab-1':
        line_graph1 = dcc.Graph(
            id='graph-1',
            figure={
                'data': [
                    {'x': data['date'], 'y': data["confirmed"], 'type': 'line', 'name': 'Confirmed Cases',
                     "mode": 'lines+markers', "marker": {"size": 4, 'symbol': 'dot', 'color': 'blue'}
                     },
                    {'x': data['date'], 'y': data["confirmed"] - data["recovered"] - data["deaths"], 'type': 'line',
                     'name': 'Active Cases',
                     "mode": 'lines+markers', "marker": {"size": 4, 'symbol': 'dot', 'color': 'gray'}
                     },
                    {'x': data['date'], 'y': data["recovered"], 'type': 'line', 'name': 'Recovered Case',
                     "mode": 'lines+markers', "marker": {"size": 4, 'symbol': 'dot', 'color': 'green'}
                     },
                    {'x': data['date'], 'y': data["deaths"], 'type': 'line', 'name': 'Deaths',
                     "mode": 'lines+markers', "marker": {"size": 4, 'symbol': 'dot', 'color': "red"}
                     },
                ],
                'layout': {
                    'legend': {'x': 0.10, 'y': 0.9},
                    'title': f'Covid19 India: Cumulative Spread Trend [Unofficial]',
                    'xaxis': x_axis,
                    'yaxis': y_axis,
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'size': 16
                    },
                    'annotations': annotations,
                }
            }
        )
        bar_daily = dcc.Graph(
            id='graph-daily',
            figure={
                'data': [
                    {'x': data['date'], 'y': data["daily_deaths"], 'type': 'bar', 'name': 'Deaths',
                     "marker": {'color': "red"},
                     },
                    {'x': data['date'], 'y': data["daily_recovered"], 'type': 'bar', 'name': 'Recovered Case',
                     "marker": {'color': "green"},
                     },
                    {'x': data['date'], 'y': data["daily_confirmed"] - data["daily_recovered"] - data["daily_deaths"],
                     'type': 'bar', 'name': 'Active Cases',
                     "marker": {'color': "blue"},
                     },
                    {"x": data['date'], "y": data['7day_mean'], "type": 'line', 'name': "7-Day Average",
                     "marker": {'color': "#171535"},
                     }
                ],
                'layout': {
                    'legend': {'x': 0.10, 'y': 0.9},
                    'title': f'Covid19 India: Daily Spread Trend [Unofficial]',
                    # 'height': 700,
                    'barmode': 'stack',
                    'xaxis': x_axis,
                    'yaxis': y_axis,
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'size': 16
                    },
                }
            }
        )

        tab_display = html.Div([html.Div(line_graph1, className='cum-cases', id='cum-cases', style={
            'display': 'inline-block',
        }),
                                html.Div(bar_daily, className='daily-cases', id="daily-cases", style={
                                    'display': 'inline-block',
                                })]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'})
        return [tab_display, data_head, state_data]

    elif tab == 'tab-2':
        week_annots = [{
            'x': i,
            'y': j + 1000,
            'showarrow': False,
            'text': f"{j}",
            "font": {"size": 14},
            'xref': 'x',
            'yref': 'y',
        } for i, j in df_itvl[['interval', 'daily_confirmed_cum_sum']].values
        ]
        bar_graph2 = dcc.Graph(
            id='bar-graph2',
            figure={
                'data': [{'x': df_itvl['interval'], 'y': df_itvl['daily_confirmed_cum_sum'] -
                                                         df_itvl['daily_recovered_cum_sum'] -
                                                         df_itvl['daily_deaths_cum_sum'], 'type': 'bar',
                          'name': 'Active Cases'},
                         {'x': df_itvl['interval'], 'y': df_itvl['daily_recovered_cum_sum'], 'type': 'bar',
                          "marker": {'color': "green"}, 'name': 'Recovered Cases'},
                         {'x': df_itvl['interval'], 'y': df_itvl['daily_deaths_cum_sum'], 'type': 'bar',
                          "marker": {'color': "red"}, 'name': 'Deaths Cases'},
                         ],
                'layout': {
                    'legend': {'x': 0.10, 'y': 0.9},
                    'title': f'Covid19 India: Cases by week',
                    'barmode': 'stack',
                    # 'height': 700,
                    'xaxis': x_axis_bar,
                    'yaxis': y_axis,
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'size': 16
                    },
                    "margin": {"l": 0, 'b': 55, "t": 50},
                    'annotations': week_annots
                }
            }
        )
        try:
            bar = df.sort_values('Total Confirmed cases')
            bar = bar[:-1]
            bar['Total'] = bar['Total Confirmed cases'] - \
                           bar["Cured/Discharged/Migrated"] - bar['Death']
            bar = bar.sort_values('Total')
            bar_graph3 = dcc.Graph(
                id='bar-graph3',
                figure={
                    'data': [{'y': bar['Name of State / UT'], 'x': bar['Total'],
                              'type': 'bar', "orientation": 'h', 'name': 'Active Cases'},
                             {'y': bar['Name of State / UT'], 'x': bar["Cured/Discharged/Migrated"], 'type': 'bar',
                              "orientation": 'h', "marker": {'color': "green"}, 'name': 'Recovered Case'},
                             {'y': bar['Name of State / UT'], 'x': bar["Death"], 'type': 'bar', "orientation": 'h',
                              'name': 'Deaths', "marker": {'color': "red"}}
                             ],
                    'layout': {
                        'legend': {'x': 0.80, 'y': 0.9},
                        'title': f'Covid19 India: Cases by State',
                        'barmode': 'stack',
                        'height': 700,
                        'xaxis': x_axis_h,
                        'yaxis': y_axis_h,
                        'plot_bgcolor': colors['background2'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text'],
                            'size': 13
                        },
                        "margin": {"l": 200, 'b': 50, "t": 50}
                    }
                }
            )

            A = html.Div(children=[bar_graph2], className='bar-graph2', id="bar-graph2",
                         style={'display': 'inline-block'})
            B = html.Div(children=[bar_graph3], className='bar-graph3', id="bar-graph3", style={"width": "98%"})
            C = html.Div(children=[test_graph], className='test-graph', id="test-graph",
                         style={'display': 'inline-block'})
            D = html.Div(children=[dist_chart], className='dist-graph', id="dist-graph", style={"width": "98%"})
            tab2_display = html.Div(children=[A, C, B, D]
                                    , className='tab2-graph', id="tab2-graph", style={'textAlign': 'center'})
            return [analysis1, tab2_display]
        except:
            return [bar_graph2]
    elif tab == 'tab-3':
        return news1
    elif tab == 'tab-4':
        return info
