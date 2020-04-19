from decouple import config
import plotly.express as px
import pandas as pd

mapbox_token = config("MAPBOX_SECRET")
mapbox_style = config("MAPBOX_STYLE")

px.set_mapbox_access_token(mapbox_token)


def scatter_mapbox(data=None):
    """
    Return Scatter map of cases of each state of India.
    :param data: (DataFrame) Data of each state
    :return: (plotly map)
    """
    df_geo = data.copy()
    states = pd.read_csv('data/states.csv')
    df_geo = pd.merge(df_geo[1:], states[['Name of State / UT', 'latitude', 'longitude']], on='Name of State / UT',
                      how='left')

    df_geo = df_geo.iloc[:-1, :]
    df_geo['Total_confirmed'] = df_geo["Total Confirmed cases"]
    # print(df_geo)
    color_scale = [
        "#fadc8f", "#f9d67a", "#f8d066", "#f8c952", "#f7c33d", "#f6bd29",
        "#f5b614", "#F4B000", "#eaa900", "#e0a200", "#dc9e00", "#FFA07A",
    ]

    # Scaled the data exponentially to show smaller values.
    df_geo["scaled"] = df_geo["Total_confirmed"] ** 0.9
    fig = px.scatter_mapbox(
        df_geo,
        lat="latitude",
        lon="longitude",
        color="Total_confirmed",
        size="scaled",
        size_max=50,
        hover_name="Name of State / UT",
        hover_data=["Total_confirmed", "Death", "Cured/Discharged/Migrated", "Name of State / UT"],
        color_continuous_scale=color_scale,
    )

    fig.layout.update(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=700,
        # width=700,
        # This takes away the color bar on the right hand side of the plot if it is set to False
        coloraxis_showscale=False,
        mapbox_style=mapbox_style,
        mapbox=dict(center=dict(lat=23.5937, lon=81.9629), zoom=4, ),
    )

    fig.data[0].update(
        hovertemplate="%{customdata[3]} <br>Confirmed: %{customdata[0]}<br>Recovered: %{customdata[2]}<br>Deaths: %{"
                      "customdata[1]} "
    )
    del df_geo, states
    return fig
