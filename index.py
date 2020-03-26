from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_daq as daq
from datetime import datetime
from data.data import COVID19India
from data.inshorts_news import InshortsNews
from data.data_processing import get_daily_data, get_interval_data
from data.map import get_map
import dash_dangerously_set_inner_html
colors = {
    'background': 'white',
    'background2': 'black',
    'text': '#000080'
}

y_axis = {
    'title': 'Cases',
    'showspikes': True,
    'spikedash': 'dot',
    'spikemode': 'across',
    'spikesnap': 'cursor',
}

x_axis = {
    'title': 'Date',
    'showspikes': True,
    'spikedash': 'dot',
    'spikemode': 'across',
    'spikesnap': 'cursor',
}

x_axis_bar = {
    'title': 'Weeks Count [Starting from 01-03-2020]',
    'showspikes': True,
    'spikedash': 'dot',
    'spikemode': 'across',
    'spikesnap': 'cursor',
}

tabs_styles = {
    'height': '51px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '2px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'black',
    'color': 'yellow',
    'padding': '10px'
}

inshorts = InshortsNews()
covidin = COVID19India()
try:
    df = covidin.moh_data(save=True)
except:
    df = pd.read_csv('data/25.03.2020_moh_india.csv')

map = get_map(data_df=df)
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
    style={'textAlign': 'right'})
], style={
    # 'textAlign': 'center',
    "background": "#CCFFFF",
    "padding": "70px 0",
})

df2 = covidin.change_cal()

data_display = """
| **Name of State / UT** | **Total Confirmed cases (Indian National)** | **Total Confirmed cases ( Foreign National )** | |**Cured/Discharged/Migrated** |  | **Death** |
|:---------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
"""
# df = df.sort_values('Total Confirmed cases (Indian National)', ascending=False)
for v1, v2 in zip(df.values, df2.values):
    a = v1[0]
    b = v1[1] if v2[1] == 0 else f"{v1[1]} (**+{v2[1]}**)"
    c = v1[2] if v2[2] == 0 else f"{v1[2]} (**+{v2[2]}**)"
    d = v1[3] if v2[3] == 0 else f"{v1[3]} (**+{v2[3]}**)"
    e = v1[4] if v2[4] == 0 else f"{v1[4]} (**+{v2[4]}**)"
    v = f"""|{a}|{b}|{c}||{d}||{e}|\n"""
    data_display += v

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

data_head = html.Div(children=[dcc.Markdown(  # markdown
    f"# COVID19 STATEWISE STATUS \n(Last updated {covidin.last_update()})")], style={
    'textAlign': 'center',
    "background": "yellow"})

# map1 = dash_dangerously_set_inner_html.DangerouslySetInnerHTML(map)
# map1 = html.A('Map', href='/static/map.html', style={'textAlign': 'center'})
map1 = html.Div(children=[dcc.Markdown(  # markdown
    "##  [Covid India Map](/static/map.html)")], style={
    'textAlign': 'center',
    "background": "black"})

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
                       html.Div(id='graph-input'),
                       dcc.Tabs(id="all-tabs-inline", value='tab-1', children=[
                           dcc.Tab(label='All Cases', value='tab-1', style=tab_style,
                                   selected_style=tab_selected_style),
                           dcc.Tab(label='Cases Analysis', value='tab-2', style=tab_style,
                                   selected_style=tab_selected_style),
                           dcc.Tab(label='News', value='tab-3', style=tab_style,
                                   selected_style=tab_selected_style),
                           dcc.Tab(label='Help and Information', value='tab-4', style=tab_style,
                                   selected_style=tab_selected_style),
                       ], style=tabs_styles,
                                colors={
                                    "border": "yellow",
                                    "primary": "red",
                                    "background": "orange"
                                }),
                       html.Div(id='graph-output'),  # Tab output
                       html.Div(id='jhu-data', style={'display': 'none'}),
                        html.Div(children=[dcc.Markdown(  # markdown
                           " Data Resources: [MInistry of Health and Family Welfare | GoI](https://www.mohfw.gov.in/)"
                           " and [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19) ")], style={
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


@app.callback(Output('jhu-data', 'children'),
              [Input('dummy-id', '')])
def get_data(_):
    try:
        df_jhu = covidin.jhu_india_data(save=False)
    except:
        df_jhu = pd.read_csv("data/jhu_india.csv")
    df_jhu['date'] = pd.to_datetime(df_jhu['date'])
    # row = [[pd.to_datetime("2020-03-26"), 471, 35, 9] ]
    # df_jhu = pd.concat([df_jhu, pd.DataFrame(row, columns=df_jhu.columns)], ignore_index=True)
    # df_jhu.to_csv('data/jhu_india.csv', index=False)
    return df_jhu.to_json(date_format='iso', orient='split')


@app.callback([Output('active-display', 'children'),
                Output('recovered-display', 'children'),
                Output('death-display', 'children'),
               Output('counts-display', 'children')
               ],
              [Input('dummy-id', '')])
def display_cases(_):
    # df = pd.read_csv('data/21.03.2020_moh_india.csv')
    value = df.values[-1][1:].tolist()
    active_case = value[0] + value[1] - value[2] - value[3]
    recovered_case = value[2]
    deaths = value[-1]
    counts = len(df) - 1

    def daq_display(value, clr):
        display = daq.LEDDisplay(
                            label={'label': "", 'style': {'font-size': "14px",
                                                             'color': 'green',
                                                             'font-family': 'sans-serif',
                                                             'background': 'black',
                                                             'padding': '2px'
                                                        }
                                   },
                            labelPosition='left',
                            value=str(value),
                            backgroundColor=clr,
                            size=18,
                            # family='sans-serif',
                            style={'display': 'inline-block',
                                   },
                        )
        return display

    a = daq_display(active_case, 'black')
    b = daq_display(recovered_case, 'green')
    c = daq_display(deaths, 'red')
    d = daq_display(counts, 'gray')

    return [a, b, c, d]


@app.callback(Output(component_id='graph-output', component_property='children'),
              [Input('jhu-data', 'children'),
               Input('all-tabs-inline', 'value')])
def render_graph(data,  tab):
    try:
        df = pd.read_json(data, orient='split')
    except:
        df = pd.read_csv('data/jhu_india.csv')
    df['date'] = pd.to_datetime(df['date'])
    date = df.date.tolist()[-1].strftime("%d-%m-%Y")
    data = df[df.date > "2020-02-29"]

    df1 = get_daily_data(df)
    df_itvl = get_interval_data(days=7, cases=df1, cols=None)

    state_data = html.Div(children=[dcc.Markdown(  # markdown
                                                   data_display)], style={
                                                   'textAlign': 'center',
                                                   "background": "#CCFFFF",
                                                   "padding": "70px 0",
                        })

    graph = dcc.Graph(
        id='graph-1',
        figure={
            'data': [
                {'x': data['date'], 'y': data["confirmed"], 'type': 'line', 'name': 'Confirmed Cases',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'cross-open'}},
                {'x': data['date'], 'y': data["recovered"], 'type': 'line', 'name': 'Recovered Case',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'star-open'}},
                {'x': data['date'], 'y': data["deaths"], 'type': 'line', 'name': 'Deaths',
                 "mode": 'lines+markers', "marker": {"size": 10, 'symbol': 'x-open'}},
            ],
            'layout': {
                'title': f'Covid19 India Cases (Updated on {date} at 11:59:59 PM)',
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

    bar_graph1 = dcc.Graph(
        id='bar-graph',
        figure={
            'data': [{'x': df1['date'], 'y': df1['confirmed'], 'type': 'bar', 'name': 'Confirmed Cases'},
                     {'x': df1['date'], 'y': df1["recovered"], 'type': 'bar', 'name': 'Recovered Case'},
                     {'x': df1['date'], 'y': df1["deaths"], 'type': 'bar', 'name': 'Deaths', 'color': 'red'}
                     ],
            'layout': {
                'title': f'Covid19 India Cases by Day',
                'barmode': 'stack',
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

    bar_graph2 = dcc.Graph(
        id='bar-graph',
        figure={
            'data': [{'x': df_itvl['interval'], 'y': df_itvl['daily_confirmed_cum_sum'], 'type': 'bar', 'name': 'Confirmed Cases'},
                     {'x': df_itvl['interval'], 'y': df_itvl['daily_recovered_cum_sum'], 'type': 'bar',
                      'name': 'Recovered Cases'},
                     {'x': df_itvl['interval'], 'y': df_itvl['daily_deaths_cum_sum'], 'type': 'bar',
                      'name': 'Deaths Cases'},
            ],
            'layout': {
                'title': f'Covid19 India Cases by week',
                'barmode': 'stack',
                'height': 700,
                'xaxis': x_axis_bar,
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

    if tab == 'tab-1':
        return [graph, data_head, state_data, map1]
    elif tab == 'tab-2':
        return [bar_graph1, bar_graph2]
    elif tab == 'tab-3':
        return news1
    elif tab == 'tab-4':
        return info


if __name__ == '__main__':
    app.run_server(debug=True)