from app import app
from app import server
import callbacks
from layouts import layout

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)