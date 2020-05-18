import dash_core_components as dcc
import dash_html_components as html

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '2px',
    'fontWeight': 'bold',
    'vertical-align': 'middle',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'white',
    'color': 'blue',
    'padding': '10px',
    "font-size": 20
}

dis = html.Div(children=
               [html.Div(className='bg-yellow', id="total",
                         children=[
                             html.Img(src='assets/images/covid.png',
                                      alt='confirm status',
                                      style={'height': '40%',
                                             'width': '40%'}),
                             html.H5(id="confirm-display"),
                             html.P('Confirm Cases')
                         ],
                         style={
                             'display': 'inline-block',
                             "textAlign": "center",
                             "width": "130px",
                         }),
                html.Div(className='bg-blue', id="active",
                         children=[
                             html.Img(src='assets/images/icon-infected.png',
                                      alt='active status'),
                             html.H5(id="active-display"),
                             html.P('Active Cases')
                         ],
                         style={
                             'display': 'inline-block',
                             "textAlign": "center",
                             "width": "140px",
                         }
                         ),
                html.Div(className='bg-green', id="cure",
                         children=[
                             html.Img(src='assets/images/icon-inactive.png',
                                      alt='cured status'),
                             html.H5(id="recovered-display"),
                             html.P('Recovered Cases')
                         ],
                         style={
                             'display': 'inline-block',
                             "textAlign": "center",
                             "width": "140px",
                         }
                         ),
                html.Div(className='bg-red', id="death",
                         children=[
                             html.Img(src='assets/images/icon-death.png',
                                      alt='death status'),
                             html.H5(id="death-display"),
                             html.P('Deaths')
                         ],
                         style={
                             'display': 'inline-block',
                             "textAlign": "center",
                             "width": "140px",
                         }
                         ),
                # html.Div(className='bg-orange', id="states", children=[html.Img(src='assets/images/india.png',
                #                                                                 alt='states UTs status',
                #                                                                 style={'height': '32%',
                #                                                                        'width': '32%'}),
                #                                                        html.H5(id='counts-display'),
                #                                                        html.P('Affected States')],
                #          style={
                #              'display': 'inline-block',
                #              "textAlign": "center",
                #              "width": "140px",
                #          }
                #          ),
                html.Div(className='bg-info', id="source",
                         children=[
                             html.A(html.Img(src='assets/images/icon-state.png',
                                             alt='states-data',
                                             style={'height': '100%',
                                                    'width': '95%'}
                                             ), href="#state-data"),
                             html.H5("Data Source"),
                             html.A("MoHFW", href='https://www.mohfw.gov.in/',
                                    style={'font-size': "23px"}),
                         ],
                         style={
                             'display': 'inline-block',
                             "textAlign": "center",
                             "width": "140px",
                         }
                         )
                ], className="data-row", style={'textAlign': 'center',
                                                'background': '#b8bdd4', 'vertical-align': 'middle'})

footer = html.Div(className='footer',
                  children=[html.Div([
                      html.Div([html.H2("Created by ",
                                        style={'display': 'inline-block',
                                               'margin': "0px",
                                               "color": 'navy',
                                               "line-height": "0.1"
                                               }
                                        ),
                                html.A(html.Img(src="assets/images/dca.png", alt="author",
                                                style={
                                                    'height': "10%",
                                                    "width": "3.75%",
                                                    'display': 'inline-block',
                                                    "border-radius": "50%",
                                                    "margin": "10px"
                                                }
                                                ),
                                       href='https://www.linkedin.com/in/dcaichara/',
                                       style={'vertical-align': 'middle'}
                                       )
                                ],
                               ),
                      html.H2("Source code available on",
                              style={'display': 'inline-block',
                                     'margin': "0px",
                                     "color": 'navy',
                                     "line-height": "0.1", }
                              ),
                      html.A(html.Img(src="assets/images/github.png",
                                      alt="github",
                                      className="git-image",
                                      style={'height': "10%",
                                             "width": "7%",
                                             'display': 'inline-block'
                                             }),
                             href='https://github.com/dc-aichara/COVID19-India-Tracker',
                             className='git-code',
                             style={'vertical-align': 'middle'})],
                  ),
                  ],
                  style={'textAlign': "center"})

layout = html.Div([html.H1("COVID19 India Tracker",
                           style={
                               'textAlign': 'center',
                               "background": "yellow"}),
                   dis,
                   html.Div(id='graph-input'),
                   dcc.Tabs(id="all-tabs-inline", className="all-tabs-inline", value='tab-1', children=[
                       dcc.Tab(label='Overview', value='tab-1', style=tab_style,
                               selected_style=tab_selected_style),
                       dcc.Tab(label='Analysis', value='tab-2', style=tab_style,
                               selected_style=tab_selected_style),
                       dcc.Tab(label='News', value='tab-3', style=tab_style,
                               selected_style=tab_selected_style),
                       dcc.Tab(label='Help and Information', value='tab-4', style=tab_style,
                               selected_style=tab_selected_style),
                   ],
                            colors={
                                "border": "yellow",
                                "primary": "red",
                                "background": "orange"
                            }),
                   html.Div(id='graph-output'),  # Tab output
                   html.Div(id='api-data', style={'display': 'none'}),
                   html.Div(id='dummy-id'),
                   html.Div(footer),
                   html.Div(children=[
                       dcc.Markdown(  # markdown
                           " #### Primary Data Sources: [Ministry of Health and Family Welfare | GoI]("
                           "https://www.mohfw.gov.in/) "
                           " and [covid19india API](https://api.covid19india.org/data.json) ")
                   ],
                       style={
                           'textAlign': 'center',
                           "background": "yellow"}
                   ),

                   ], style={
    "background": "#000080"}
                  )
