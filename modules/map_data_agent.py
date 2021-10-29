import os
import datetime
import json
import lat_lng_code_generator


class MapDataAgent:
    def __init__(self, echo=True, echo_error=True):
        self.echo = echo
        self.echo_error = echo_error
        self.current_path = os.path.dirname(__file__)

    def log(self, content):
        if self.echo:
            print('MapDataAgent> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('MapDataAgent> \033[91m{}'.format(content) + '\033[0m')

    def _createKey(self, dict, key):
        if key not in dict.keys():
            dict[key] = []

    def _createDir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def _loadData(self, type, lon_code, lat_code):
        file_path = "{}/../data/{}_data/dist/{}/{}.json".format(
            self.current_path, type, lon_code, lat_code)
        if not os.path.isfile(file_path):
            self.errlog("data not exist.")
            return -1
        with open(file_path, "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
        self.log("{} data loaded: LON: {}; LAT: {}".format(
            type, lon_code, lat_code))
        return data

    # def createDBType(self, service_name):
    #     distribution_data = self._saveLatLngCodeData(service_name)
    #     giant_data = {}
    #     key_list = []
    #     file_list = os.listdir(
    #         "{}/../data/bldg_data/raw/{}".format(os.path.dirname(__file__), service_name))
    #     for file_name in file_list:
    #         with open("{}/../data/bldg_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, file_name), "r", encoding="utf-8") as f:
    #             data = json.load(f)
    #         for key in data[0].keys():
    #             key_list.append(key)
    #         for each_data in data:
    #             pnu = each_data["NSDI:PNU"]
    #             latlng = distribution_data[pnu]
    #             lat, lng = latlng["lat_code"], latlng["lng_code"]
    #             if pnu not in giant_data.keys():
    #                 giant_data[pnu] = {"lat_code": lat, "lng_code": lng}
    #             for key, val in each_data.items():
    #                 giant_data[pnu][key] = val
    #     key_list = set(key_list)
    #     scheme = {}
    #     for key in key_list:
    #         if ("_PCLND" in key) or ("_code" in key):
    #             scheme[key] = "int"
    #         else:
    #             scheme[key] = "str"
    #     dict_list = {"scheme": scheme, "data": giant_data}
    #     with open("{}/../output/bldg_data_db_type.json".format(os.path.dirname(__file__)), "w", encoding="utf-8") as f:
    #         json.dump(dict_list, f, indent=4, ensure_ascii=False)
    ["id", "service_name", "LND_SHAPE"]
    ["id", transaction.list 중 id가 제일 큰거의 "NRG_DL_M", "NRF_DL_D", "NRG_AR_"]
    ["id", "service_name", "MAP_SHAPE", MAP]
    # MAP_LAT MAP_LON

    def create(self, service_name_list):
        self._createDir(self.current_path+'/../data/map_data')
        self._createDir(self.current_path+'/../data/map_data/raw')
        config_data = self._getConfig("land_service")
        for service in service_name_list:
            input_list = []
            input_list_seperated = []
            for key, val in config_data[service]["organized_pnu_list"].items():
                input_list.append(
                    {"pnu": key, "filter_output": val})
            sep_key_list = self._getSeperatedPnuList(
                config_data[service]["organized_pnu_list"].keys())
            for sep_key in sep_key_list:
                input_list_seperated.append(
                    {"sigunguCd": sep_key["sigunguCd"], "bjdongCd": sep_key["bjdongCd"]})
            # self.log(input_list)
            # self.log(input_list_seperated)
            self._createDir(self.current_path +
                            '/../data/bldg_data/raw/{}'.format(service))
            self.get_api.getApi(
                self.current_path+'/../data/bldg_data/raw/{}'.format(service), input_list)
            self.get_api_by_seperated_pnu.getApi(
                self.current_path+'/../data/bldg_data/raw/{}'.format(service), input_list_seperated)
            self.distributeDataByLonLat(service)
        self.log("data successfully distributed")


if __name__ == "__main__":
    bldg_data_agent = MapDataAgent()
    # print(land_data_agent.handleLandServiceConfigFromFile("pnu_list"))
    # bldg_data_agent.create(["YBD", "GBD", "CBD"])
    # bldg_data_agent.create(["TEST"])
    # bldg_data_agent.create(["CBD"])
    # bldg_data_agent.distributeDataByLonLat("GBD")
    # bldg_data_agent.distributeDataByLonLat("CBD")
    # bldg_data_agent.distributeDataByLonLat("YBD")
    # bldg_data_agent.distributeDataByLonLat("TEST")
    # land_data_agent.createDBType("GBD")
    # print(bldg_data_agent._getSeperatedPnu("1101202030"))
    bldg_data_agent._loadData("land", "50764", "15010")
    bldg_data_agent._loadData("transaction", "50764", "15010")
