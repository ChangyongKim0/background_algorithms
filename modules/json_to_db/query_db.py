import mysql.connector
import configparser
import json
import os
try:
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
except:
    ABS_PATH = os.getcwd()
config = configparser.ConfigParser()
data_dir = f"{ABS_PATH}/data"
config.read(f"{data_dir}/args.txt")

db_user = config['database']['user']
db_pwd = config['database']['pwd']
db_name = config['database']['name']
con = mysql.connector.connect(
    user=db_user,
    password=db_pwd,
    host="127.0.0.1",
    port=3306,
    database=db_name,
)
cursor = con.cursor()

table_name = "land_data"
query = f"select lat_code, lng_code from {table_name};"
cursor.execute(query)
result = cursor.fetchall()
print(result)