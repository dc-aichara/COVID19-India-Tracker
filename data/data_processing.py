import pandas as pd
import numpy as np


def get_daily_data(df):
    df1 = df[df['date'] > "2020-02-29"].reset_index(drop=True)

    def get_daily_cases(x):
        a = [x[0]] + np.diff(x).tolist()
        return a

    df1['daily_confirmed'] = get_daily_cases(df1.confirmed)
    df1['daily_recovered'] = get_daily_cases(df1.recovered)
    df1['daily_deaths'] = get_daily_cases(df1.deaths)
    return df1


def get_interval_data(days=7, cases=pd.DataFrame(), cols=None):
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
    return data
