import json
import sqlite3
import pandas as pd
from src.SQLite import connectBD, insertTable
from src.legal import parseLegalJson
from src.users import parseUsersInfo, parseUsersDatesIps
from src.utils import readJson

con = connectBD()
#legal_table = parseLegalJson()
#insertTable(con, legal_table, "legal")

users_table_info = parseUsersInfo()
users_table_ips_dates = parseUsersDatesIps()

insertTable(con, users_table_info, "users_info")
insertTable(con, users_table_ips_dates, "users_ips_dates")
