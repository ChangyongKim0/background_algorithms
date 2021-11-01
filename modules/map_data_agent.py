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

    def _getLonLatList(self):
        lon_lat_list = {}
        lon_list = os.listdir(
            "{}/../data/land_data/dist".format(self.current_path))
        for lon in lon_list:
            lat_list = os.listdir(
                "{}/../data/land_data/dist/{}".format(self.current_path, lon))
            lon_lat_list[lon] = [lat.split(".")[0] for lat in lat_list]
        return lon_lat_list

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
    # ["id", "service_name", "LND_SHAPE"]
    # ["id", transaction.list 중 id가 제일 큰거의 "NRG_DL_M", "NRF_DL_D", "NRG_AR_"]
    # ["id", "service_name", "MAP_SHAPE", MAP]
    # MAP_LAT MAP_LON

    def create(self):
        self._createDir(self.current_path+'/../data/map_data')
        lon_lat_list = self._getLonLatList()
        for lon, lat_list in lon_lat_list.items():
            self._createDir(self.current_path+'/../data/map_data/'+lon)
            for lat in lat_list:
                map_data = {}
                land_data_list = self._loadData("land", lon, lat)
                transaction_data_list = self._loadData("transaction", lon, lat)
                for land_data in land_data_list:
                    map_data[land_data["id"]] = {
                        "id": land_data["id"], "sevice_name": land_data["service_name"], "LND_SHAPE": land_data["LND_SHAPE"]}
                if transaction_data_list != -1:
                    for transaction_data in transaction_data_list:
                        map_data[transaction_data["id"]
                                 ]["transaction_list"] = transaction_data["transaction_list"]
                map_data = [*map_data.values()]
                with open("{}/../data/map_data/{}/{}.json".format(self.current_path, lon, lat), "w", encoding="utf-8") as f:
                    json.dump(map_data, f, indent=4, ensure_ascii=False)
        self.log("data successfully distributed")


if __name__ == "__main__":
    map_data_agent = MapDataAgent()
    # map_data_agent._loadData("land", "50764", "15010")
    # map_data_agent._loadData("transaction", "50764", "15010")
    # print(map_data_agent._getLonLatList())
    map_data_agent.create()
