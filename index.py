import callbacks
from app import app, server
from layouts import layout

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)
