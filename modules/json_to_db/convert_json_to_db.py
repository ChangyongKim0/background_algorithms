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

json_file_name = f"{ABS_PATH}/data/land_data_db_type.json"
with open(json_file_name, 'r') as f:
    json_data = json.load(f)
scheme_dict = json_data['scheme']
scheme_dict['id'] = 'VARCHAR(20)'
scheme_dict['lat_code'] = 'FLOAT'
scheme_dict['lng_code'] = 'FLOAT'
for key, value in scheme_dict.items():
    if value == 'str':
        value = 'TEXT'
        scheme_dict[key] = value

table_name = 'land_data'
column_list = list(scheme_dict.keys())
type_list = list(scheme_dict.values())
assert 'id' in column_list

land_data = json_data['data']
id_list = list(land_data.keys())
for id in id_list:
    item_dict = land_data[id]

    query = f'insert into {table_name} ('
    query2 = " VALUES ("
    for column in column_list:
        if column == 'id':
            value = id
        else:
            value = item_dict[column]

        query += f"`{column}`, "
        if type(value) == dict:
            query2 += f"NULL, "
        else:
            query2 += f"'{value}', "
    if len(column_list) > 0:
        query = query[:-2]
        query2 = query2[:-2]
    query += ")"
    query2 += ");"
    query += query2

    print(f"[Database / insert] table: {table_name}, id: {id}")
    cursor.execute(query)
    con.commit()