import os
import datetime
import json
import api_agent
import math


class LandDataAgent:
    def __init__(self, echo=True, echo_error=True):
        self.get_api = api_agent.ApiAgent("land")
        self.echo = echo
        self.echo_error = echo_error

    def log(self, content):
        if self.echo:
            print('LandDataAgent> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('LandDataAgent> \033[91m{}'.format(content) + '\033[0m')

    def _createKey(self, dict, key):
        if key not in dict.keys():
            dict[key] = []

    def _getOrganizedPnu(self, pnu_list):
        organized_pnu_list = {}
        for pnu in pnu_list:
            naive_pnu = str(int(pnu)//100)
            self._createKey(organized_pnu_list, naive_pnu)
            organized_pnu_list[naive_pnu].append(pnu)
        return organized_pnu_list

    def _getOrganizedPnuFromFile(self, file_name):
        with open("{}/../input/{}.txt".format(os.path.dirname(__file__), file_name), "r") as f:
            lines = f.read().splitlines()
        return self.getOrganizedPnu(lines)

    def _getConfig(self, file_name):
        with open("{}/../configs/{}.json".format(os.path.dirname(__file__), file_name), "r") as f:
            return json.load(f)

    def _getToday(self):
        return datetime.date.today().strftime('%Y%m%d')

    def _createBackUp(self, file_name, action_name, new_data):
        print(1)

    def _updateConfig(self, file_name, new_data):
        with open("{}/../configs/{}.json".format(os.path.dirname(__file__), file_name), "w") as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)

    def handleLandServiceConfig(self, action, service_name, pnu_list=[]):
        config_data = self._getConfig("land_service")
        base_date = self._getToday()
        organized_pnu_list = self._getOrganizedPnu(pnu_list)

        if service_name in config_data.keys():
            if action == "create":
                self.errlog(
                    "the service already exist. Create after delete it.")
                return -1

        config_data[service_name] = {"base_date": base_date,
                                     "organized_pnu_list": organized_pnu_list}

        self._createBackUp("land_service", action, config_data[service_name])

        self._updateConfig("land_service", config_data)

    def handleLandServiceConfigFromFile(self, file_name):
        with open("{}/../input/{}.txt".format(os.path.dirname(__file__), file_name), "r") as f:
            lines = f.read().splitlines()
        service_name = lines.pop(1)
        action = lines.pop(0)
        self.handleLandServiceConfig(action, service_name, lines)

    # def _getAuthKey(self, api_type):
    #     with open("{}/../security/authkey.json".format(os.path.dirname(__file__)), "r") as f:
    #         auth_key = json.load(f)
    #     return auth_key[api_type]

    # def _getApiKeyList(self, api_type):
    #     with open("{}/../configs/api_preset.json".format(os.path.dirname(__file__)), "r") as f:
    #         auth_key = json.load(f)
    #     return auth_key["api_key_list"][api_type]
    def _createDir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def _getLatLngCode(self, feature_string, threshold):
        latlng_list = feature_string.split(" ")
        lat_list = [float(latlng_list[2*i])
                    for i in range(len(latlng_list)//2)]
        lng_list = [float(latlng_list[2*i+1])
                    for i in range(len(latlng_list)//2)]
        return str(math.floor(min(lat_list)*threshold)), str(math.floor(min(lng_list)*threshold))

    def _saveLatLngCodeData(self, service_name):
        file_path = "{}/../data/land_data/raw/{}".format(
            os.path.dirname(__file__), service_name)
        if not os.path.isfile(file_path+"/land_char_WFS.json"):
            self.errlog(
                "cannot find land_char_WFS.json file, thus cannot load feature data.")
            return -1
        with open(file_path+"/land_char_WFS.json", "r", encoding='UTF8') as f:
            data = json.load(f)
        distribution_data = {}
        for each_data in data:
            lat, lng = self._getLatLngCode(each_data["gml:posList"], 400)
            distribution_data[each_data["NSDI:PNU"]] = {
                "lat_code": lat, "lng_code": lng}
        return distribution_data

    def _distributeDataByLonLat(self, service_name):
        distribution_data = self._saveLatLngCodeData(service_name)
        if distribution_data == -1:
            return -1
        file_list = os.listdir(
            "{}/../data/land_data/raw/{}".format(os.path.dirname(__file__), service_name))
        giant_data = {}
        for file_name in file_list:
            with open("{}/../data/land_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)
            for each_data in data:
                pnu = each_data["NSDI:PNU"]
                latlng = distribution_data[each_data["NSDI:PNU"]]
                lat, lng = latlng["lat_code"], latlng["lng_code"]
                if lat not in giant_data.keys():
                    giant_data[lat] = {}
                if lng not in giant_data[lat].keys():
                    giant_data[lat][lng] = {}
                if pnu not in giant_data[lat][lng].keys():
                    giant_data[lat][lng][pnu] = {
                        "pnu": pnu, "service_name": service_name}
                giant_data[lat][lng][pnu][file_name.split(".")[0]] = each_data
        file_path = "{}/../data/land_data".format(os.path.dirname(__file__))
        dist_file_path = self._createDir(file_path+"/dist")
        for lat, lat_data in giant_data.items():
            self._createDir(dist_file_path+"/"+lat)
            for lng, lng_data in lat_data.items():
                data_list = []
                for val in lng_data.values():
                    data_list.append(val)
                with open("{}/{}/{}.json".format(dist_file_path, lat, lng), "w", encoding="utf-8") as f:
                    json.dump(data_list, f, indent=4, ensure_ascii=False)

    def create(self, service_name_list):
        config_data = self._getConfig("land_service")
        input_list = []
        for service in service_name_list:
            for key, val in config_data[service]["organized_pnu_list"].items():
                input_list.append({"pnu": key, "filter_output": val})
            self.get_api.getApi(
                "{}/../data/land_data/raw/{}".format(os.path.dirname(__file__), service), input_list)
            self._distributeDataByLonLat(service)
        self.log("data successfully distributed")


if __name__ == "__main__":
    land_data_agent = LandDataAgent()
    # print(land_data_agent.handleLandServiceConfigFromFile("pnu_list"))
    # land_data_agent.create(["GBD"])
    land_data_agent._distributeDataByLonLat("GBD")
