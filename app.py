import dash

external_stylesheets = ["static/css/style.css", 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('COVID19 India Tracker', external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'Coronavirus (COVID19) India Tracker'

