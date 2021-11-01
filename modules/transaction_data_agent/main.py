from database import Database

from copy import deepcopy
import numpy as np
import datetime
import sqlite3
import json
import time
import glob
import csv
import os


class TrDataParser:
    column_list = ['시군구', '유형', '지번', '도로명', '용도지역', '건축물주용도', '도로조건',
                   '전용/연면적(㎡)', '대지면적(㎡)', '거래금액(만원)', '층', '계약년월', '계약일', '지분구분', '건축년도', '해제사유발생일']
    address_idx = column_list.index('시군구')
    type_idx = column_list.index('유형')
    number_idx = column_list.index('지번')
    road_idx = column_list.index('도로명')
    found_idx = column_list.index('건축년도')
    area_idx = column_list.index('전용/연면적(㎡)')
    price_idx = column_list.index('거래금액(만원)')
    year_idx = column_list.index('계약년월')
    day_idx = column_list.index('계약일')

    def __init__(self):
        self.data_dir = 'data/transaction'
        self.database = Database("propi")
        self.database.verbose = False

    def parseTrData(self):
        transaction_list = []
        dir_list = glob.glob(f'{self.data_dir}/*')
        dir_list.sort()
        for dir_idx in range(len(dir_list)):
            dir_name = dir_list[dir_idx]
            sub_dir_list = glob.glob(f"{dir_name}/*")
            sub_dir_list.sort()

            for file_idx in range(len(sub_dir_list)):
                file_name = sub_dir_list[file_idx]
                # print(file_name)

                data = []
                with open(file_name, 'r') as f:
                    rdr = csv.reader(f)
                    for line in rdr:
                        assert len(line) in [1, 16]
                        if len(line) == 16:
                            data.append(line)

                equal = True
                for i in range(16):
                    if data[0][i] != self.column_list[i]:
                        equal = False
                        break
                assert equal

                transaction_list += data[1:]
        return transaction_list

    def buildingFilter(self, transaction_item):
        if transaction_item[self.type_idx] in ["일반"]:
            first = f"{transaction_item[self.address_idx]} {transaction_item[self.number_idx].replace('*', '')}"
            # print(first)
            second = transaction_item[self.road_idx]
            third = transaction_item[self.found_idx]
            fourth = transaction_item[self.area_idx]
            filter_dict = {'first': first, 'second': second,
                           'third': third, 'fourth': fourth}
            filter_results = self.database.queryFilter(
                'building_filter', filter_dict)
        else:
            filter_results = []
        return filter_results

    def createBuildingFilter(self):
        results = self.database.queryAll(table_name='building')
        for result_idx in range(len(results)):
            id = results[result_idx]['id']

            first = results[result_idx]['BLRD_PLC']
            first = first.split(' ')
            first[-1] = first[-1][0:1]
            first = ' '.join(first)

            second = results[result_idx]['BLRD_PLC_N']
            if second is not None:
                second = second.split(' ')[2]

            third = results[result_idx]['BLRD_DT_APR']
            third = f"{third}"[:4]

            fourth = results[result_idx]['BLRD_TOTA_AR']

            insert_dict = {'id': id, 'first': first,
                           'second': second, 'third': third, 'fourth': fourth}
            self.database.insert('building_filter', insert_dict)

    def landFilter(self, transaction_item):
        print("WE NEED LANDFILTER!!!")
        # raise NotImplementedError

    def filter(self, transaction_item):
        results = self.buildingFilter(transaction_item)
        NRG_AR = transaction_item[self.area_idx]
        NRG_DL_AM = transaction_item[self.price_idx]
        NRG_DL_M = transaction_item[self.year_idx]
        NRG_DL_D = transaction_item[self.day_idx]
        id = f"{NRG_DL_M}{NRG_DL_D}"
        filter_result = {'id': id, 'NRG_AR': NRG_AR, 'NRG_DL_AM': NRG_DL_AM,
                         'NRG_DL_M': NRG_DL_M, 'NRG_DL_D': NRG_DL_D}
        if len(results) == 0:
            filter_result['address_id'] = "unclassified"
            filter_result['service_name'] = "No information"
        elif len(results) > 1:
            self.landFilter(transaction_item)
            print("RESULT IS:", result)
            print("FILTERED RESULT IS:", filter_result)
            return -1
        else:
            filter_results = self.database.queryFilter(
                'building', {'id': results[0]['id']})
            assert len(filter_results) == 1
            address_id = filter_results[0]['address_id']

            filter_dict = {'id': address_id}
            ba_results = self.database.queryFilter(
                'building_address', filter_dict)
            assert len(ba_results) == 1
            filter_result['address_id'] = ba_results[0]['id']
            filter_result['service_name'] = ba_results[0]['service_name']
        return filter_result


if __name__ == "__main__":
    tr_data_parser = TrDataParser()

    transaction_list = tr_data_parser.parseTrData()

    # tr_data_parser.createBuildingFilter() # 빌딩 업데이트 후 필수로 만들어야 함

    complete_list = []

    for transaction_item in transaction_list:
        result = tr_data_parser.filter(transaction_item)
        if result == -1:
            continue

        complete_idx = None
        for idx, item in enumerate(complete_list):
            if item['id'] == result['address_id']:
                complete_idx = idx
                break
        if complete_idx is None:
            complete_list.append({
                'id': result['address_id'],
                'service_name': result['service_name'],
                'transaction_list': []
            })
            complete_idx = len(complete_list) - 1

        complete_list[complete_idx]['transaction_list'].append({
            'id': result['id'],
            'NRG_AR': result['NRG_AR'],
            'NRG_DL_AM': result['NRG_DL_AM'],
            'NRG_DL_M': result['NRG_DL_M'],
            'NRG_DL_D': result['NRG_DL_D'],
        })

    with open("match_result.json", "w", encoding='utf-8') as json_file:
        json.dump(complete_list, json_file, indent=4)
