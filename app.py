import dash
import flask
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('COVID19 India Tracker', external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'COVID19 India Tracker'


@server.route('/')
def favicon():
    return flask.send_from_directory(os.path.join(server.root_path, 'static'),
                                     'favicon.ico')
