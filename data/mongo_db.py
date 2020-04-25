from decouple import config
import pandas as pd
import pymongo
from datetime import datetime, timedelta

date = (datetime.today()-timedelta(days=1)).strftime("%Y.%m.%d")
date1 = (datetime.today()).strftime("%Y.%m.%d")

mgdb_user = config("MGDB_user")
mgcb_pass = config('MGDB_pass')
server = f"mongodb+srv://{mgdb_user}:{mgcb_pass}@testcluster-cntgf.mongodb.net/admin"
# server = f"mongodb+srv://{mgdb_user}:{mgcb_pass}@testcluster-cntgf.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(server)

db = client.test_data
collection = db.test1


def upload_data(data=None, _id=None):
    """
    Upload a pandas DataFrame to MangoDB
    :param data: (DataFrame) Pandas DataFrame
    :param _id: (str) unique id for data eg., date
    """
    dic = {'id': _id}
    for col in data.columns:
        dic[col] = list(data[col].values.astype(str))
    if collection.find_one({'id': _id}) is None:
        collection.insert(dic)
    else:
        collection.replace_one({'id': _id}, dic)


def get_data(id_=None):
    """
    Get data from MangoDB by filter
    :param id_: (str) id
    :return: Pandas DataFrame
    """
    data = collection.find_one({'id': id_})
    if data is not None:
        data = pd.DataFrame(data)
        del data['_id'], data['id']

        for col in data.columns[1:]:
            data[col] = data[col].astype(int)
        return data
    return


