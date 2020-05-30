import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import datetime, timedelta
from data.mongo_db import upload_data, get_data

moh_link = "https://www.mohfw.gov.in/"
url_state = "https://api.covid19india.org/state_district_wise.json"
data_data = "https://api.covid19india.org/data.json"


class COVID19India(object):
    """
    Covid19 India data module
    """

    def __init__(self):
        self.moh_url = moh_link  # MOHFW website link
        self.url_state = url_state  # districtwise data
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
        del df["S. No."]
        del df["Active Cases*"]
        df = df.dropna()
        df.columns = [re.findall('[a-zA-Z /]+', k)[0] for k in df.columns]
        df = df[['Name of State / UT', 'Total Confirmed cases', 'Cured/Discharged/Migrated', 'Deaths']]
        df.columns = ['Name of State / UT', 'Total Confirmed cases', 'Cured/Discharged/Migrated', 'Death']
        cols = df.columns.values.tolist()
        for col in cols[1:]:
            try:
                idx = list(df[cols[0]]).index('West Bengal') + 1
                df = df[: idx + 1]
                df[col] = df[col].apply(lambda x: int(re.findall('[0-9]+', str(x))[0]))
            except:
                df = df[:-1]
                df[col] = df[col].apply(lambda x: int(re.findall('[0-9]+', str(x))[0]))
        df = df.sort_values('Total Confirmed cases', ascending=False)
        df = df.reset_index(drop=True)
        df.iloc[0, 0] = "Total"
        df['Name of State / UT'] = [re.findall("[a-zA-Z ]+", x)[0] for x in df['Name of State / UT']]
        while save:
            content = self.__request(url)

            soup = BeautifulSoup(content, 'html.parser')
            text = soup.find_all('div', attrs={'class': 'status-update'})[0].text.strip()
            date = pd.to_datetime(text.split(':')[1].split(',')[0]).strftime('%Y.%m.%d')
            # df.to_csv(f"data/{date}_moh_india.csv", index=False)
            upload_data(df, date)
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

    @staticmethod
    def change_cal():
        """
        Calculation changes in cases from previous day (MoHFW data)
        :return: (DataFrame)
        """
        date = (datetime.today() - timedelta(days=1)).strftime("%Y.%m.%d")  # Previous day's date
        date0 = (datetime.today()).strftime("%Y.%m.%d")  # Today's date
        a = get_data(date0)
        if a is not None:
            b = get_data(id_=date)
        else:
            date0 = (datetime.today() - timedelta(days=1)).strftime("%Y.%m.%d")
            date = (datetime.today() - timedelta(days=2)).strftime("%Y.%m.%d")
            a = get_data(date0)
            b = get_data(date)
        lst = []
        for name in a['Name of State / UT'].values:
            if name in b['Name of State / UT'].values:
                c = (a[a['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                d = (b[b['Name of State / UT'] == name]).values[0][1:].astype(np.int64)
                lst.append([name] + list(abs(c - d)))
            else:
                c = list((a[a['Name of State / UT'] == name]).values[0])
                lst.append(c)
        df2 = pd.DataFrame(data=lst, columns=a.columns)
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
                c = state_data[k]['districtData'][k2]
                try:
                    v = [k, k2, c.get('confirmed'), c.get('active'), c.get("deceased"), c.get('recovered')]
                except:
                    v = [k, k2, c.get('confirmed')]
                Values.append(v)
        try:
            state_data = pd.DataFrame(Values,
                                      columns=['State_UT', 'District', 'Confirmed', 'Active', 'Deaths', 'Recovered'])
        except:
            state_data = pd.DataFrame(Values,
                                      columns=['State_UT', 'District', 'Confirmed'])
        state_data = state_data[state_data['Confirmed'] >= 0]
        return state_data

    def StateWise_data(self):
        """
        Statewise data (total cases and new cases data)
        :return: (DataFrames) Statewise data (total cases and new cases data)
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        # print(data['statewise'])
        data_state = [[v['state'],
                       v['confirmed'],
                       v['active'],
                       v['recovered'],
                       v['deaths'],
                       v['lastupdatedtime']]
                      for v in data['statewise']]

        data_state1 = [[v['state'],
                        v['deltaconfirmed'],
                        v['deltarecovered'],
                        v['deltadeaths'],
                        v['lastupdatedtime']]
                       for v in data['statewise']]

        states = pd.DataFrame(data=data_state, columns=['state_ut', 'confirmed', 'active',
                                                        'recovered', 'deaths', 'last_updated'])
        states_new = pd.DataFrame(data=data_state1, columns=['state_ut', 'confirmed',
                                                             'recovered', 'deaths', 'last_updated'])
        return states, states_new

    def timeseries_data(self):
        """
        TimeSeries covid19 data of India
        :return: (DataFrame) TimeSeries covid19 data of India
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        tm = [list(v.values()) for v in data['cases_time_series']]
        tm = pd.DataFrame(tm, columns=data['cases_time_series'][0].keys())

        return tm

    def current_update(self):
        """
        Latest covid19 cases data
        :return: (json) Latest covid19 cases data
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        # data = data["key_values"]
        return data

    def tests(self):
        """
        Test statistics
        :return: (DataFrame) Test counts and results by day
        """
        content = self.__request(self.data_url)
        data = json.loads(content)
        values = [list(v.values())[-5:] for v in data['tested']]
        for v in data['tested']:
            values.append(list(v.values())[-5:])
        data = pd.DataFrame(values, columns=list(data['tested'][0].keys())[-5:])
        return data
