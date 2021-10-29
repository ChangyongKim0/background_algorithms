from database import Database

from copy import deepcopy
import numpy as np
import datetime
import sqlite3
import json
import time
import glob
import os

if __name__ == "__main__":
    database = Database("propi")

    land_column_list = None
    land_type_list = None
    for table_info in database.table_info_list:
        if table_info['name'] == "land":
            land_column_list = table_info['column_list']
            land_type_list = table_info['type_list']
            break

    dir_list = glob.glob('data/land/dist/*')
    for dir_idx in range(len(dir_list)):
        dir_name = dir_list[dir_idx]
        file_list = glob.glob(f"{dir_name}/*")

        for file_idx in range(len(file_list)):
            file_name = file_list[file_idx]
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)

            temp_dir_name = dir_name.replace(
                '\\', '/').split('/')[-1].split('.')[0]
            temp_file_name = file_name.replace(
                '\\', '/').split('/')[-1].split('.')[0]

            for land_data in data:
                insert_dict = dict()
                for column_idx, column in enumerate(land_column_list):
                    if column == "dir_name":
                        item = temp_dir_name
                    elif column == "file_name":
                        item = temp_file_name
                    else:
                        item = land_data[column]
                    if type(item) == dict:
                        item = None

                    types = land_type_list[column_idx]
                    if item is not None and types == "text":
                        item = item.replace('"', '').replace("'", '')

                    if item is not None:
                        try:
                            if item == "ZZ":
                                int(1)
                            elif types == "int":
                                int(item)
                            elif types == "float":
                                float(item)
                        except:
                            print(types, column, item)
                            raise ValueError

                    insert_dict[column] = item

                results = database.queryFilter("land", filter_dict=insert_dict)
                if len(results) == 0:
                    database.insert("land", insert_dict=insert_dict)
