from app import app
from app import server
import callbacks
import dash_dangerously_set_inner_html
from layouts import layout

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)