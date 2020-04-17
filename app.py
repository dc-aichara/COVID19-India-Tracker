import dash

external_stylesheets = ["static/css/style.css", 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash('COVID19 India Tracker', external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = 'Coronavirus (COVID19) India Tracker'

########################################################################
#
#  For Google Analytics
#
########################################################################
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-3QRH180VJK"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-163694740-1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta property="og:type" content="article">
        <meta property="og:title" content="Coronavirus (COVID19) India Tracker">
        <meta property="og:site_name" content="https://covid19-india-tracker.herokuapp.com/ ">
        <meta property="og:url" content="https://covid19-india-tracker.herokuapp.com/ ">
        <meta property="og:image" content="https://raw.githubusercontent.com/dc-aichara/COVID19-India-Tracker/master/assets/favicon.ico">
        <meta property="article:published_time" content="2020-03-21">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

