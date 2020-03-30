import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "assets/css/table.css"]
app = dash.Dash('COVID19 India Tracker', external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'COVID19 India Tracker'

