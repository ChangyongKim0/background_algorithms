from copy import deepcopy
import numpy as np
import datetime
import sqlite3
import json
import time
import glob
import os

class Database:
    def __init__(self, db_name="propi", log_dir=None):
        self.name = db_name
        is_created, self.con, self.cursor, self.table_info_list = self.connect(db_name)
        if not is_created: self.create()
        # self._create('building_filter')
        self.verbose = True

    def connect(self, db_name):
        save_dir = './data'
        file_name = f"{db_name}.db"
        # get database
        is_created = True if os.path.exists('{}/{}'.format(save_dir, file_name)) else False
        con = sqlite3.connect('{}/{}'.format(save_dir, file_name))
        cursor = con.cursor()

        table_info_list = []
        if db_name == "propi":
            table_name = 'building'
            column_list = [
                'id', 'BLRD_IDNTF', 'BLRD_PRPS_MJ', 'BLRD_PRPS_MJ_NM', 'BLRD_PRPS_ETC_NM', 
                'BLRD_RF', 'BLRD_RF_NM', 'BLRD_RF_ETC', 'BLRD_HHLD', 'BLRD_FMLY', 
                'BLRD_HO', 'BLRD_HG', 'BLRD_FL_GR', 'BLRD_FL_UGR', 'BLRD_EL_USE', 
                'BLRD_EL_EME', 'BLRD_Atch_BLD', 'BLRD_Atch_AR', 'BLRD_TOT_AR', 'BLRD_PR_MC_IN', 
                'BLRD_PR_MC_IN_AR', 'BLRD_PR_MC_OT', 'BLRD_PR_MC_OT_AR', 'BLRD_PR_AT_IN', 'BLRD_PR_AT_IN_AR', 
                'BLRD_DT_PMS', 'BLRD_DT_STC', 'BLRD_DT_APR', 'BLRD_EN_GR', 'BLRD_EN_RT', 
                'BLRD_EN_EPI', 'BLRD_GN_GR', 'BLRD_GN_CRT', 'BLRD_IT_GR', 'BLRD_IT_CRT', 
                'BLRD_DT_CRTN', 'BLRD_PLC', 'BLRD_PNU_SGG', 'BLRD_PNU_BJD', 'BLRD_PNU_GB', 
                'BLRD_PNU_BUN', 'BLRD_PNU_JI', 'BLRD_RG_CD', 'BLRD_RG_CD_NM', 'BLRD_RG_KN_CD', 
                'BLRD_RG_KN_CD_NM', 'BLRD_NM', 'BLRD_DNM', 'BLRD_PLC_N', 'BLRD_SPL_N', 
                'BLRD_LOT_CNT', 'BLRD_RD_CD', 'BLRD_RD_BJD', 'BLRD_RD_UGR', 'BLRD_RD_MB', 
                'BLRD_RD_SB', 'BLRD_Atch_CD', 'BLRD_Atch_CD_NM', 'BLRD_PL_AR', 'BLRD_ARC_AR', 
                'BLRD_BC_RAT', 'BLRD_TOTA_AR', 'BLRD_TOTA_FL_AR', 'BLRD_FL_RAT', 'BLRD_STR_CD', 
                'BLRD_STR_ETC', 'BLRD_QK_YN', 'BLRD_QK_AB', 'address_id'
            ]
            type_list = [
                'text', 'text', 'text', 'text', 'text', 
                'int', 'text', 'text', 'int', 'int', 
                'int', 'float', 'int', 'int', 'int', 
                'int', 'int', 'float', 'float', 'int', 
                'float', 'int', 'float', 'int', 'float', 
                'int', 'text', 'int', 'text', 'float', 
                'int', 'text', 'int', 'text', 'int', 
                'int', 'text', 'int', 'int', 'int', 
                'int', 'int', 'int', 'text', 'int', 
                'text', 'text', 'text', 'text', 'text', 
                'int', 'int', 'int', 'int', 'float', 
                'float', 'int', 'text', 'float', 'float', 
                'float', 'float', 'float', 'float', 'int', 
                'text', 'int', 'text', 'text'
            ]
            table_info_list.append({'name':table_name, 'column_list':column_list, 'type_list':type_list})

            table_name = 'building_address'
            column_list = ['id', 'service_name', 'dir_name', 'file_name']
            type_list = ['text', 'text', 'text', 'text']
            table_info_list.append({'name':table_name, 'column_list':column_list, 'type_list':type_list})

            table_name = 'building_filter'
            column_list = ['id', 'first', 'second', 'third', 'fourth']
            type_list = ['text', 'text', 'text', 'text', 'float']
            table_info_list.append({'name':table_name, 'column_list':column_list, 'type_list':type_list})

            table_name = 'land'
            column_list = [
                'id', 'service_name', 'LNOD_PNU', 'LNOD_PS', 'LNOD_LBL', 
                'LNOD_N', 'LNOD_AG', 'LNOD_RS', 'LNOD_CH', 'LNOD_CH_DT', 
                'LNOD_NT', 'LNOD_STD_DT', 'LNSD_PNU', 'LNSD_PRP_DSTRC', 'LNSD_PRP_DSTRC_NM', 
                'LNSD_PRP_CNF', 'LNSD_STD_DT', 'LND_PNU', 'LND_SHAPE', 'LND_Regstr_CODE', 
                'LND_CGR', 'LND_CGR_NM', 'LND_AR', 'LND_USE', 'LND_USE_NM', 
                'LND_HG', 'LND_HG-NM', 'LND_FR', 'LND_FR_NM', 'LND_RD', 
                'LND_RD_NM', 'LND_STD_DT', 'LNPD_PNU', 'LNPD_YR', 'LNPD_MT', 
                'LNPD_ST', 'LNPD_PY0', 'LNPD_PY1', 'LNPD_PY2', 'LNPD_PY3', 
                'LNPD_PY4', 'LNPD_STD', 'dir_name', 'file_name'
            ]
            type_list = [
                'int', 'text', 'int', 'int', 'text', 
                'int', 'text', 'text', 'int', 'int', 
                'text', 'text', 'int', 'text', 'text', 
                'text', 'text', 'int', 'text', 'int', 
                'int', 'text', 'float', 'int', 'text', 
                'int', 'text', 'int', 'text', 'int', 
                'text', 'text', 'int', 'int', 'int', 
                'int', 'int', 'int', 'int', 'int', 
                'int', 'text', 'text', 'text'
            ]
            table_info_list.append({'name':table_name, 'column_list':column_list, 'type_list':type_list})

        else:
            raise ValueError("The db name is wrong.")
        return is_created, con, cursor, table_info_list        

    def create(self):
        for table_info in self.table_info_list:
            table_name = table_info['name']
            column_list = table_info['column_list']
            type_list = table_info['type_list']
            query = f'CREATE TABLE {table_name}('
            for i in range(len(column_list)):
                column_name = column_list[i]
                type_name = type_list[i]
                query += f"`{column_name}` {type_name}, "
            column_name = column_list[-1]
            type_name = type_list[-1]
            query += "PRIMARY KEY (id));"
            self.cursor.execute(query)
            self.con.commit()

    def _create(self, table_name):
        column_list = None
        type_list = None
        for table_info in self.table_info_list:
            if table_info['name'] == table_name:
                column_list = table_info['column_list']
                type_list = table_info['type_list']
                break
        query = f'CREATE TABLE {table_name}('
        for i in range(len(column_list)):
            column_name = column_list[i]
            type_name = type_list[i]
            query += f"`{column_name}` {type_name}, "
        column_name = column_list[-1]
        type_name = type_list[-1]
        query += "PRIMARY KEY (id));"
        self.cursor.execute(query)
        self.con.commit()

    def parsing(self, table_name, result):
        column_list = None
        for table_info in self.table_info_list:
            if table_info['name'] == table_name:
                column_list = table_info['column_list']
                break

        parsed_list = []
        for item in result:
            parsed_dict = dict()
            # for i in range(len(item) - 1):
            for i in range(len(item)):
                parsed_dict[column_list[i]] = item[i]
            # parsed_dict['id'] = item[-1]
            parsed_list.append(parsed_dict)
        return parsed_list

    def queryFilter(self, table_name, filter_dict):
        filter_list = []
        for key in filter_dict.keys():
            filter_list.append([key, filter_dict[key]])

        query = f"select * from {table_name} where"
        cnt = 0
        for filter in filter_list:
            column, value = filter
            if value is None:
                continue
            query += f" `{column}`='{value}' and"
            cnt += 1
        if cnt > 0:
            query = query[:-4] + ';'
        if self.verbose: print(f"[Database / query] table name : {table_name}, query : {query}")
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return self.parsing(table_name, result)

    def queryAll(self, table_name):
        query = f"select * from {table_name};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return self.parsing(table_name, result)

    def update(self, table_name, key_name, key_value, update_dict):
        query = f'update {table_name} set '
        for column in update_dict.keys():
            value = update_dict[column]
            if value is None:
                query += f"`{column}`=NULL, "
            else:
                query += f"`{column}`='{value}', "
        if len(update_dict.keys()) > 0:
            query = query[:-2]
        query += f" where {key_name}='{key_value}';"
        if self.verbose: print(f"[Database / update] table name : {table_name}, query : {query}")
        self.cursor.execute(query)
        self.con.commit()

    def insert(self, table_name, insert_dict):
        column_list = None
        for table_info in self.table_info_list:
            if table_info['name'] == table_name:
                column_list = table_info['column_list']
                break

        query = f'insert into {table_name} ('
        query2 = " VALUES ("
        for column in insert_dict.keys():
            value = insert_dict[column]
            query += f"`{column}`, "
            if value is None:
                query2 += f"NULL, "
            else:
                query2 += f"'{value}', "
        if len(column_list) > 0:
            query = query[:-2]
            query2 = query2[:-2]
        query += ")"
        query2 += ");"
        query += query2
        # if self.verbose: print(f"[Database / insert] table name : {table_name}, query : {query}")
        try: self.cursor.execute(query)
        except: print("data already exist.")
        self.con.commit()
