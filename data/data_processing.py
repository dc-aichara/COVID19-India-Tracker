import pandas as pd
import numpy as np
import re
from pathlib import Path


def get_daily_data(df):
    """
    Clean daily data
    :param df: (DataFrame)
    :return: (DataFrame) Cleaned DataFrame
    """
    df1 = df[df['date'] > "2020-02-29"].reset_index(drop=True)

    def get_daily_cases(x):
        a = [x[0]] + np.diff(x).tolist()
        return a

    df1['daily_confirmed'] = get_daily_cases(df1.confirmed)
    df1['daily_recovered'] = get_daily_cases(df1.recovered)
    df1['daily_deaths'] = get_daily_cases(df1.deaths)
    df1["7day_mean"] = df1.daily_confirmed.rolling(7).mean().fillna(0).astype(int)
    return df1


def get_interval_data(days=7, cases=pd.DataFrame(), cols=None):
    """
    Get data by a interval (days9
    :param days: (int) Number of days
    :param cases: (DataFrame)
    :param cols: (Columns of DataFrame)
    :return: (DataFrame)
    """
    if cols is None:
        cols = ["daily_confirmed", 'daily_recovered', 'daily_deaths']
    data = {}
    value = "week" if days == 7 else f"{days}days"
    for i in range(len(cases)):
        if i % days == 0:
            a = int(i / days) + 1
            data[value + '-' + str(a)] = [cases[col][i:i + days].sum() for col in cols]

    data = pd.DataFrame(data=[[k] + v for k, v in data.items()], columns=['interval'] + cols)
    for col in cols:
        data[col + "_cum_sum"] = data[col].cumsum()
    # print(data)
    return data


def get_state_daily():
    """
    State cases
    :return: (json) Statewise cases by data
    """
    p = Path("Data/")

    files = sorted([f for f in list(Path.glob(p, '*.csv')) if "moh" in f.parts[-1]])

    states = pd.read_csv("data/states.csv")

    daily_data = {}

    for value in states['Name of State / UT'].values:
        daily_data[value] = {"Date": [], 'Total Confirmed cases': [],
                             'Cured/Discharged/Migrated': [], 'Death': []}

    for f in files:
        df = pd.read_csv(f)
        date = re.findall("[0-9.]+", f.parts[-1])[0]
        for k in daily_data.keys():
            if k in df['Name of State / UT'].values:
                v = df[df['Name of State / UT'] == k].values[0]
                daily_data[k]['Date'].append(date)
                daily_data[k]['Total Confirmed cases'].append(v[1])
                daily_data[k]['Cured/Discharged/Migrated'].append(v[2])
                daily_data[k]['Death'].append(v[3])

    return daily_data

