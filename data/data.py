import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from pathlib import Path
now = datetime.today().strftime("%d-%m-%Y")

jhu_links = {'confirmed': "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv",
             'deaths': "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv",
             'recovered': "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
             }
moh_link = "https://www.mohfw.gov.in/"


class COVID19India():

    def __init__(self):
        self.jhu_links = jhu_links
        self.moh_link = moh_link

    def jhu_india_data(self, save=False):
        data = pd.DataFrame()
        for key, link in self.jhu_links.items():
            df = pd.read_csv(link)
            df = df[df["Country/Region"] == "India"]
            data["date"] = df.columns.values.tolist()[4:]
            data[key] = df.values[0].tolist()[4:]

        data['date'] = pd.to_datetime(data['date'])
        while save:
            date = data.date.tolist()[-1].strftime("%d-%m-%Y")
            data.to_csv(f"{date}_jhu_india.csv", index=False)
            break
        return data

    def moh_data(self, save=False):
        url = self.moh_link
        df = pd.read_html(url)[-1]
        del df['S. No.']
        while save:
            content = requests.get(url).content.decode('utf-8')

            soup = BeautifulSoup(content, 'html.parser')
            text = [text.text for text in soup.find_all('p') if 'as on' in text.text][-1]
            date = re.findall('[0-9.]+', text)[0]
            df.to_csv(f"{date}_moh_india.csv", index=False)
            break
        return df

    def last_update(self):
        content = requests.get(url).content.decode('utf-8')

        soup = BeautifulSoup(content, 'html.parser')
        text = [text.text for text in soup.find_all('p') if 'as on' in text.text][-1]
        text = re.findall('[a-zA-Z0-9.:]+', text)
        text = " ".join(text[text.index('on'):])
        return  text

    def change_cal(self):
        p1 = Path('')
        files = list(p1.glob('*.csv'))
        f_path = []
        for file in files:
            print(file.parts)
            if 'moh' in file.parts[-1]:
                f_path.append(file)

        df = pd.read_csv(f_path[-1])
        df1 = pd.read_csv(f_path[-2])

        for name in df['Name of State / UT'].values:
            if name in df1['Name of State / UT'].values:
                a = (df[df['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                b = (df1[df1['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                lst.append([name] + list(a - b))
            else:
                a = list((df[df['Name of State / UT'] == name]).values[0])
                lst.append(a)
        df2 = pd.DataFrame(data=lst, columns=df.columns)
        return df2

