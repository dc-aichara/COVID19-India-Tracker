import dash_core_components as dcc
import dash_html_components as html

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
    'backgroundColor': 'white',
    'color': 'blue',
    'padding': '10px',
    "font-size": 20
}


layout = html.Div([html.H1("COVID19 India Tracker",
                               style={
                                   'textAlign': 'center',
                                   "background": "yellow"}),
                       html.Div([
                                 html.Span("Confirmed Cases: "),
                                 html.Div(id='confirm-display', style={'display': 'inline-block', 'font-size': 12}),
                                 html.Span("Active Cases: "),
                                 html.Div(id='active-display', style={'display': 'inline-block', 'font-size': 12}),
                                html.Span("Recovered Cases: "),
                                html.Div(id='recovered-display', style={'display': 'inline-block', 'font-size': 12}),
                                html.Span("Deaths: "),
                                html.Div(id='death-display', style={'display': 'inline-block', 'font-size': 12}),
                                html.Span("Affected States and UTs: "),
                                html.Div(id='counts-display', style={'display': 'inline-block', 'font-size': 12}),
                                html.A("(MoHFW)", href='https://www.mohfw.gov.in/', style={'display': 'inline-block', 'font-size': 24})
                                 ], className="row ",
                                style={
                                    'marginTop': 1, 'marginBottom': 2, 'font-size': 30, 'color': 'white',
                                    'display': 'inline-block', "position": "auto"
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
                       html.Div(id='api-data', style={'display': 'none'}),
                        html.Div(children=[dcc.Markdown(  # markdown
                           "Primary Data Resources: [Ministry of Health and Family Welfare | GoI]("
                           "https://www.mohfw.gov.in/) "
                           " and [covid19india API](https://api.covid19india.org/data.json) ")], style={
                           'textAlign': 'center',
                           "background": "yellow"}),
                       html.Div(children=[dcc.Markdown(  # markdown
                           "© 2020 [DCAICHARA](https://github.com/dc-aichara/COVID19-India-Tracker)  All Rights "
                           "Reserved.")], style={
                           'textAlign': 'center',
                           "background": "yellow"}),
                       html.Div(id='dummy-id'),

                       ], style={
    "background": "#000080"}
                      )
