import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime
from pathlib import Path

now = datetime.today().strftime("%d-%m-%Y")
moh_link = "https://www.mohfw.gov.in/"
url_state = "https://api.covid19india.org/state_district_wise.json"
data_india = "https://www.covid19india.org/india.json"
data_data = "https://api.covid19india.org/data.json"


class COVID19India(object):

    def __init__(self):
        self.moh_url = moh_link  # MOHFW website
        self.url_state = url_state  # districtwise data
        self.india_url = data_india  # India map
        self.data_url = data_data  # All India data ==> Statewise data, test data, timeseries data etc

    def __request(self, url):
        """
        Requests get method to extract data
        :param url: Link to data api or website
        :return: api/link content
        """
        content = requests.get(url).content.decode('utf-8')
        return content

    def moh_data(self, save=False):
        """
        Get lasted data from Ministry of Health and Family Welfare | GOI
        :param save: (bool)
        :return: (DataFrame) Statewise data
        """
        url = self.moh_url
        df = pd.read_html(url)[-1]
        del df['S. No.']
        cols = df.columns.values.tolist()
        for col in cols[1:]:
            try:
                if df['Name of State / UT'].values[-1] != "Total number of confirmed cases in India":
                    df = df[:-1]
                df[col] = df[col].apply(lambda x: int(re.findall('[0-9]+', str(x))[0]))
            except:
                df = df[:-1]
                df[col] = df[col].apply(lambda x: int(re.findall('[0-9]+', str(x))[0]))
        while save:
            content = self.__request(url)

            soup = BeautifulSoup(content, 'html.parser')
            text = soup.find_all('div', attrs={'class': 'status-update'})[0].text.strip()
            date = pd.to_datetime(text.split(':')[1].split(',')[0]).strftime('%d.%m.%Y')
            df.to_csv(f"data/{date}_moh_india.csv", index=False)
            break
        return df

    def last_update(self):
        """
        Last data update on MoHFW | GOI website
        :return: (str) Last Update date and time
        """
        content = self.__request(self.moh_url)

        soup = BeautifulSoup(content, 'html.parser')
        text = soup.find_all('div', attrs={'class': 'status-update'})[0].text.strip()
        text = text.split(" : ")[-1]
        return text

    def change_cal(self):
        """
        Calculation changes in cases from previous day (MoHFW data)
        :return: (DataFrame)
        """
        p1 = Path('data/')
        files = list(p1.glob('*.csv'))
        f_path = []
        for file in files:
            if 'moh' in file.parts[-1]:
                f_path.append(file)
        # print(f_path)
        f_path = sorted(f_path)
        df = pd.read_csv(f_path[-1])
        df1 = pd.read_csv(f_path[-2])
        lst = []
        a, b = [df, df1] if len(df) > len(df1) else [df1, df]
        # print(a.shape, b.shape)
        for name in a['Name of State / UT'].values:
            if name in b['Name of State / UT'].values:
                c = (a[a['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                d = (b[b['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                lst.append([name] + list(abs(c - d)))
            else:
                c = list((a[a['Name of State / UT'] == name]).values[0])
                lst.append(c)
        df2 = pd.DataFrame(data=lst, columns=df.columns)
        return df2

    def state_district_data(self):
        """
        Districtwise data of each state
        :return: (DataFrame) districtwise data of each state
        """

        content = self.__request(self.url_state)
        state_data = json.loads(content)
        key1 = state_data.keys()
        Values = []
        for k in key1:
            key2 = state_data[k]['districtData'].keys()
            for k2 in key2:
                c = list(state_data[k]['districtData'][k2].values())
                try:
                    v = [k, k2, c[1], c[0], c[2], c[4]]
                except:
                    v = [k, k2, c[0]]
                Values.append(v)
        try:
            state_data = pd.DataFrame(Values,
                                      columns=['State_UT', 'District', 'Confirmed', 'Active', 'Deaths', 'Recovered'])
        except:
            state_data = pd.DataFrame(Values,
                                      columns=['State_UT', 'District', 'Confirmed'])
        return state_data

    def StateWise_data(self):
        """
        Statewise data (total and new data)
        :return: (Dataframes) Statewise data (total and new data)
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        data_state = []
        for v in data['statewise']:
            v = [v['state'],
                 v['confirmed'],
                 v['active'],
                 v['recovered'],
                 v['deaths'],
                 v['lastupdatedtime']]
            data_state.append(v)

        data_state1 = []
        for v in data['statewise']:
            v = [v['state'],
                 v['delta']['confirmed'],
                 v['delta']['active'],
                 v['delta']['recovered'],
                 v['delta']['deaths'],
                 v['lastupdatedtime']]
            data_state1.append(v)

        states = pd.DataFrame(data=data_state, columns=['state_ut', 'confirmed', 'active',
                                                        'recovered', 'deaths', 'last_updated'])
        states_new = pd.DataFrame(data=data_state1, columns=['state_ut', 'confirmed', 'active',
                                                             'recovered', 'deaths', 'last_updated'])
        return states, states_new

    def timeseries_data(self):
        """
        TimeSeries covid19 data of India
        :return: (DataFrame) TimeSeries covid19 data of India
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        tm = []
        for v in data['cases_time_series']:
            v = list(v.values())
            tm.append(v)

        tm = pd.DataFrame(tm, columns=data['cases_time_series'][0].keys())

        return tm

    def current_update(self):
        """
        Lastest covid19 cases counts
        :return: (json) Lastest covid19 cases
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        data = data["key_values"]
        return data

    def tests(self):
        """
        Test statistics
        :return: (DataFrame) Test counts and results by day
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        values = []
        for v in data['tested']:
            values.append(list(v.values())[1:])
        data = pd.DataFrame(values, columns=list(v.keys())[1:])
        return data
