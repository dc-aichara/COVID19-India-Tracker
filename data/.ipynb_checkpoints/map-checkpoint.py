import pandas as pd
import folium


def get_map(data_df):
    """
    Create and save map as html
    :param data_df: (DataFrame)
    :return: (html)
    """
    states = pd.read_csv('data/states.csv')

    df_geo = pd.merge(data_df[1:], states[['Name of State / UT', 'latitude', 'longitude']], on='Name of State / UT',
                      how='left')

    df_geo = df_geo.iloc[:-1, :]
    # print(df_geo)
    df_geo['Total_confirmed'] = df_geo["Total Confirmed cases"]

    colordict = {0: '#FFA07A', 1: '#FA8072',
                 2: '#E9967A', 3: '#F08080',
                 4: '#CD5C5C',
                 #             }
                 5: '#DC143C',
                 6: '#B22222', 7: '#FF0000',
                 8: "#8B0000", 9: "#800000"}
    df_geo['TC_quartile'] = pd.qcut(df_geo['Total_confirmed'], 5, labels=False)

    latitude = 20.5937
    longitude = 78.9629
    covid_map = folium.Map(location=[latitude, longitude], zoom_start=4.5)
    geo_data = zip(df_geo['latitude'], df_geo['longitude'],
                   df_geo['Total_confirmed'], df_geo['Cured/Discharged/Migrated'],
                   df_geo['Death'], df_geo['Name of State / UT'],
                   df_geo['TC_quartile'])

    for lat, lon, tc, crrd, dth, name, bins in geo_data:
        folium.CircleMarker(
            [lat, lon],
            radius=0.05 * tc,
            popup=("<strong style='color:orange;'>" + 'State/UT: ' + "</strong>" + str(name).capitalize() + '<br>'
                    "<strong style='color:orange;'>" + "Total Confirmed: " + "</strong>" + "<strong style='color:blue;'>" + str(
                tc) + "</strong>" + '<br>'
                    "<strong style='color:orange;'>" + 'Cured: ' + "</strong>" + "<strong style='color:green;'>" + str(
                crrd) + "</strong>" + "<br>"
                    "<strong style='color:orange;'>" + "Deaths: " + "</strong>" + "<strong style='color:red;'>" + "</strong>" + str(
                dth)
                   ),
            color='red',
            key_on=bins,
            threshold_scale=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            fill_color=colordict[bins],
            fill=True,
            fill_opacity=0.7
        ).add_to(covid_map)
    covid_map.save('static/map.html')
    # html_string = covid_map.get_root().render()
    # html_string = covid_map._repr_html_()
    # return html_string

