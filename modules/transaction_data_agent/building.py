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
    # database.verbose = False

    building_column_list = None
    building_type_list = None
    for table_info in database.table_info_list:
        if table_info['name'] == "building":
            building_column_list = table_info['column_list']
            building_type_list = table_info['type_list']
            break

    dir_list = glob.glob('data/building/dist/*')
    for dir_idx in range(len(dir_list)):
        dir_name = dir_list[dir_idx]
        file_list = glob.glob(f"{dir_name}/*")

        for file_idx in range(len(file_list)):
            file_name = file_list[file_idx]
            with open(file_name, "r", encoding="utf-8") as f:
                data = json.load(f)

            for each_data in data:
                bldg_list = each_data['bldg_list']
                attach_pnu_list = each_data['attach_pnu_list']
                service_name = each_data['service_name']
                address_id = each_data['id']

                temp_dir_name = dir_name.replace(
                    '\\', '/').split('/')[-1].split('.')[0]
                temp_file_name = file_name.replace(
                    '\\', '/').split('/')[-1].split('.')[0]
                insert_dict = {'id': address_id, 'service_name': service_name,
                               'dir_name': temp_dir_name, 'file_name': temp_file_name}
                results = database.queryFilter(
                    "building_address", filter_dict=insert_dict)
                if len(results) == 0:
                    database.insert("building_address",
                                    insert_dict=insert_dict)

                for bldg in bldg_list:
                    insert_dict = dict()
                    for column_idx, column in enumerate(building_column_list):
                        if column == "address_id":
                            item = address_id
                        else:
                            item = bldg[column]
                        types = building_type_list[column_idx]
                        if item is not None and types == "text":
                            item = item.replace('"', '').replace(
                                "'", '').replace("\n", ' ')
                        # if item is not None:
                        #     try:
                        #         if types == "int":
                        #             int(item)
                        #         elif types == "float":
                        #             float(item)
                        #     except:
                        #         print(types, column, item)
                        #         raise ValueError

                        insert_dict[column] = item

                    results = database.queryFilter(
                        "building", filter_dict=insert_dict)
                    if len(results) == 0:
                        database.insert("building", insert_dict=insert_dict)
