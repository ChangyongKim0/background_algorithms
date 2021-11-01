import os
import json


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
