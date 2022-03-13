import mysql.connector
import configparser
import json
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
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

    query = f'CREATE TABLE {table_name}('
    for i in range(len(column_list)):
        column_name = column_list[i]
        type_name = type_list[i]
        query += f"`{column_name}` {type_name}, "
    query += "PRIMARY KEY (`id`));"
    cursor.execute(query)
    con.commit()

    query = f'ALTER TABLE {table_name} convert to charset utf8;'
    cursor.execute(query)
    con.commit()
