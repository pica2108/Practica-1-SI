import json
import sqlite3
import pandas as pd
from src.SQLite import connectBD, insertTable
from src.legal import parseLegalJson
from src.utils import readJson

con = connectBD()
legal_table = parseLegalJson()
insertTable(con, legal_table, "legal")
