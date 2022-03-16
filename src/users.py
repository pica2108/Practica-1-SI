import numpy as np
import pandas as pd

from src.utils import readJson


def parseUsersInfo():
    data_users = readJson("./data/users.json")
    data_username_list = []
    for users_username in data_users['usuarios']:
        username = list(users_username.keys())[0]
        user_info = users_username[username]
        del user_info["ips"]
        del user_info["fechas"]
        user_info['username'] = username
        data_username_list.append(user_info)
    return pd.json_normalize(data_username_list)



def parseUsersDatesIps():
    data_users = readJson("./data/users.json")
    df_ips_dates = pd.DataFrame()
    for users_username in data_users['usuarios']:
        username = list(users_username.keys())[0]
        user_info = users_username[username]
        aux = {
            "ips": np.array(user_info["ips"]),
            "dates": np.array(user_info["fechas"]),
            "username": username
        }
        df_aux = pd.DataFrame(aux)
        df_ips_dates = pd.concat([df_ips_dates, df_aux])
    return df_ips_dates