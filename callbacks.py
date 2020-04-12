from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
import dash_daq as daq
import plotly.graph_objects as go
from datetime import datetime
from app import app
import pandas as pd
import numpy as np
from data.map import get_map
from data.data import COVID19India
from data.inshorts_news import InshortsNews
from data.data_processing import get_daily_data, get_interval_data, get_state_daily
from styles import colors, y_axis, x_axis, x_axis_bar, y_axis_h, x_axis_h, y_axis_p, x_axis_p
inshorts = InshortsNews()
covidin = COVID19India()
daily_state = get_state_daily()


try:
    df = covidin.moh_data(save=True)
except:
    df = pd.read_csv('data/2020.04.12_moh_india.csv')

# Create map
map = get_map(data_df=df)

df2 = covidin.change_cal()

data_display = """
| **Name of State / UT** | **Total Confirmed cases** |**Cured/Discharged/Migrated** | **Death** |
|:---------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
"""
# df = df.sort_values('Total Confirmed cases', ascending=False)
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

map1 = html.Div(children=[dcc.Markdown(  # markdown
    "##  [Covid India Map](/static/map.html)")], style={
    'textAlign': 'center',
    "background": "black"})

# Daily tests
tests = covidin.tests()
tests = tests[tests['totalpositivecases'] != ""]
tests['positive_rate'] = round((tests['totalpositivecases'].astype(int)/tests["totalsamplestested"].astype(int))*100, 2)
tests['updatetimestamp'] = pd.to_datetime(tests['updatetimestamp'].apply(lambda x: x.split(": ")[0]))

# New on corona virus
try:
    news_data = inshorts.get_news()
except:
    news_data = pd.DataFrame(data=["", ""], columns=['headings', 'news'])

news = """
"""
for v in news_data.values[:15]:
    if 'corona' in v[1] or 'covid' in v[1]:
        news += f"\n## {v[0]} \n#### ``` {v[1]} ```\n***"

news1 = html.Div(children=[dcc.Markdown(  # markdown
    news),
    dcc.Markdown(  # markdown
        '# **Source:**  [InShorts](https://www.inshorts.com/en/read/)',
        style={'textAlign': 'right', "white-space": "pre", "overflow-x": "scroll"})
], style={
    # 'textAlign': 'center',
    "background": "#CCFFFF",
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


@app.callback(Output('api-data', 'children'),
              [Input('dummy-id', '')])
def get_data(_):
    try:
        df_api = covidin.timeseries_data()
        df_api['date'] = pd.to_datetime(df_api['date'] + '2020')
        df_api = df_api[df_api['dailyconfirmed'] != ""]
        df_api = df_api[["date", "totalconfirmed", "totalrecovered", "totaldeceased", 'dailyconfirmed', 'dailyrecovered', 'dailydeceased']]
        df_api.columns = ['date', 'confirmed', 'recovered', 'deaths', 'daily_confirmed', 'daily_recovered', 'daily_deaths']
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


df_100 = pd.DataFrame(data={'days': [i for i in range(0, 100)]})
s100 = df[df["Total Confirmed cases"] > 200]['Name of State / UT'].values[1:].tolist()
for s in s100:
    df_s = pd.DataFrame([v for v in daily_state[s]['Total Confirmed cases'] if v >= 200], columns=[s])
    df_100 = pd.concat([df_100, df_s], 1)
l = len(df_100[df_100['Maharashtra'] > 0])
df_100 = df_100[:l]


@app.callback(Output(component_id='graph-output', component_property='children'),
              [Input('api-data', 'children'),
               Input('all-tabs-inline', 'value')])
def render_graph(data, tab):
    try:
        df_daily = pd.read_json(data, orient='split')
    except:
        df_daily = pd.read_csv('data/api_india.csv')
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    date = df_daily.date.tolist()[-1].strftime("%d-%m-%Y")
    data = df_daily[df_daily.date > "2020-02-29"]

    df1 = get_daily_data(df_daily)
    df_itvl = get_interval_data(days=7, cases=df1, cols=None)
    state_data = html.Div(children=[dcc.Markdown(  # markdown
        data_display)],
        style={
        'textAlign': 'center',
        "background": "#bccad0",
        "padding": "10px 0",
        "white-space": "pre", "overflow-x": "scroll"
    })
    dates_index = [6, 13, 20, 27, 34, 41]
    annotations = [{
        'x': pd.to_datetime(data['date'].values[i]),
        'y': data['confirmed'].values[i],
        'showarrow': True,
        'text': f"Week{j + 1 }: {data['confirmed'].values[i]}",
        "font": {"color": 'red', 'size': 12},
        'xref': 'x',
        'yref': 'y',
    } for j, i in enumerate(dates_index)]

    if tab == 'tab-1':
        line_graph1 = dcc.Graph(
            id='graph-1',
            figure={
                'data': [
                    {'x': data['date'], 'y': data["confirmed"], 'type': 'line', 'name': 'Confirmed Cases',
                     "mode": 'lines+markers', "marker": {"size": 4, 'symbol': 'dot', 'color': 'blue'}
                     },
                    {'x': data['date'], 'y': data["confirmed"]-data["recovered"]-data["deaths"], 'type': 'line',
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
                    # 'height': 700,
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
                    {'x': data['date'], 'y': data["daily_confirmed"] - data["daily_recovered"] - data["daily_deaths"] , 'type': 'bar', 'name': 'Active Cases',
                     "marker": {'color': "blue"},
                     },
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
                                                                                # 'textAlign': 'center',
                                                                                'display': 'inline-block',
                                                                                # "verticalAlign": "top",
                                                                                 }),
                                html.Div(bar_daily, className='daily-cases', id="daily-cases", style={
                                                                                # 'textAlign': 'center',
                                                                                'display': 'inline-block',
                                                                                # "verticalAlign": "top",
                                                                                 })]
                               , className='tab1-graph', id="tab1-graph", style={'textAlign': 'center'})
        return [tab_display, data_head, state_data, map1]

    elif tab == 'tab-2':
        # annots = [{
        #     'x': len(df_100[s].values[~np.isnan(df_100[s].values)]) - 0.75,
        #     'y': int(df_100[s].values[~np.isnan(df_100[s].values)][-1]),
        #     'showarrow': False,
        #     'text': f"{s}",
        #     "font": {"size": 10},
        #     'xref': 'x',
        #     'yref': 'y',
        # } for s in s100
        # ]
        # annots.append({
        #     'x': df_100['days'].values[-1] - 1,
        #     'y': 100,
        #     'showarrow': False,
        #     'text': f"Number of days since 200th case",
        #     "font": {"color": 'black', "size": 16},
        #     'xref': 'x',
        #     'yref': 'y',
        # })
        #
        # line_graph2 = dcc.Graph(
        #     id='graph-p',
        #     figure={
        #         'data': [
        #             {'x': df_100['days'], 'y': df_100[s],
        #              'type': 'line', 'name': s,
        #              "mode": 'lines+markers', "marker": {"size": 5, 'symbol': 'circle'}} for s in s100],
        #         'layout': {
        #             'title': f'Confirmed Case Trajectories by States (>200)',
        #             'height': 700,
        #             'xaxis': x_axis_p,
        #             'yaxis': y_axis_p,
        #             'plot_bgcolor': colors['background2'],
        #             'paper_bgcolor': colors['background'],
        #             'font': {
        #                 'color': colors['text'],
        #                 'size': 18
        #             },
        #             'annotations': annots,
        #         }
        #     }
        # )
        t = df.values[0][1:]
        piev = [t[0], t[0] - t[1] - t[2], t[1], t[2]]
        fig = go.Figure(go.Sunburst(
            labels=["Covid19", "Confirmed", "Active", "Recovered", "Deaths", ],
            parents=["", "Covid19", "Confirmed", "Covid19", "Covid19"],
            values=[0] + piev,
            marker=dict(
                # colors=["blue", 'gray', 'orange', 'yellow', 'red'],
                colors=[a/piev[0]*100 for a in [0] + piev],
                colorscale='RdBu',
                cmid=50
            ),
            hovertemplate='<b> %{label} Cases <br> </b> %{value} (%{color:.2f} %)',
            name='1'
        ))
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0),
                          title='Covid19 India Cases Distribution',
                          height=280,
                          width=410,
                          paper_bgcolor='#eae2e2',
                          font={'size': 16}
                          )
        pie = dcc.Graph(id='pie-chart', figure=fig)
        analysis1 = html.Div([html.Div(children=
                                       [html.Div(className="r-rate", id='rrate',
                                                 children=[html.H5("Recover Rate", style={'color': 'green'}),
                                                           html.H5(f"{piev[2]/piev[0]:.2%}"),
                                                           ],
                                                 style={
                                                     "textAlign": "center",
                                                     "width": "140px",
                                                 }
                                                 ),
                                        html.Div(className="d-rate", id='drate',
                                                 children=[html.H5("Death Rate", style={'color': 'red'}),
                                                           html.H5(f"{piev[3]/piev[0]:.2%}"),
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
                                                           ],
                                                 style={
                                                     "textAlign": "center",
                                                     "width": "140px",
                                                 }
                                                 ),
                                        html.Div(className="d-rate", id='drate',
                                                 children=[html.H5("Death Rate", style={'color': 'red'}),
                                                           html.H5(f"{piev[3] / (piev[2] + piev[3]):.2%}"),
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
                             className="row", style={
                                                    # 'display': 'inline-block',
                                                     'background': '#eae2e2',
                                                    'textAlign': 'center'})

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
                    'title': f'Covid19 India Cases by week',
                    'barmode': 'stack',
                    # 'height': 700,
                    'xaxis': x_axis_bar,
                    'yaxis': y_axis,
                    'plot_bgcolor': colors['background2'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'size': 16
                    }
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
                        'title': f'Covid19 India Cases by State',
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
            A = html.Div(bar_graph2, className='bar-graph2', id="bar-graph2", style={"width": "100%"
            })
            B = html.Div(bar_graph3, className='bar-graph3', id="bar-graph3", style={"width": "100%"
            })
            return [analysis1, A, B]
        except:
            return [bar_graph2]
    elif tab == 'tab-3':
        return news1
    elif tab == 'tab-4':
        return info
