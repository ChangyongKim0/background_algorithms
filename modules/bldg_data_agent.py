import os
import datetime
import json
import api_agent
import math
import code_translator
import identification_number_generator
import lat_lng_code_generator


class BldgDataAgent:
    def __init__(self, echo=True, echo_error=True):
        self.get_api = api_agent.ApiAgent("building")
        self.get_api_by_seperated_pnu = api_agent.ApiAgent(
            "building_registration")
        self.code_translator = code_translator.CodeTranslator()
        self.id_generator = identification_number_generator.IdentificationNumberGenerator()
        self.echo = echo
        self.echo_error = echo_error
        self.current_path = os.path.dirname(__file__)

    def log(self, content):
        if self.echo:
            print('BldgDataAgent> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('BldgDataAgent> \033[91m{}'.format(content) + '\033[0m')

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
        with open("{}/../input/{}.txt".format(os.path.dirname(__file__), file_name), "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return self.getOrganizedPnu(lines)

    def _getConfig(self, file_name):
        with open("{}/../configs/{}.json".format(os.path.dirname(__file__), file_name), "r", encoding="utf-8") as f:
            return json.load(f)

    def _getToday(self):
        return datetime.date.today().strftime('%Y%m%d')

    def _createBackUp(self, file_name, action_name, new_data):
        print(1)

    def _updateConfig(self, file_name, new_data):
        with open("{}/../configs/{}.json".format(os.path.dirname(__file__), file_name), "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=4, ensure_ascii=False)

    def _createDir(self, dir_path):
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        return dir_path

    def _distributeDataByLonLat(self, service_name):
        code_gen = lat_lng_code_generator.LatLngCodeGenerator(service_name)
        file_list = os.listdir(
            "{}/../data/bldg_data/raw/{}".format(os.path.dirname(__file__), service_name))
        giant_data = {}
        for file_name in file_list:
            api_type = file_name.split(".")[0]
            with open("{}/../data/bldg_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)
            for each_data in data:
                id_data = self.id_generator.convert(api_type, each_data)
                self.log(id_data)
                pnu = id_data["id"]
                latlng = code_gen.get(pnu)
                if latlng == -1:
                    break
                lat, lng = latlng["lat_code"], latlng["lng_code"]
                if lat not in giant_data.keys():
                    giant_data[lat] = {}
                if lng not in giant_data[lat].keys():
                    giant_data[lat][lng] = {}
                if pnu not in giant_data[lat][lng].keys():
                    giant_data[lat][lng][pnu] = {
                        "id": pnu, "service_name": service_name, "bldg_list": []}
                if id_data["id_count"] > 1:
                    each_data_converted = {
                        "id_2": id_data["id_2"], "service_name": service_name}
                    for each_key, each_val in each_data.items():
                        each_data_converted[self.code_translator.translate(
                            api_type, each_key)] = each_val
                    giant_data[lat][lng][pnu]["bldg_list"].append(
                        each_data_converted)
                else:
                    for each_key, each_val in each_data.items():
                        giant_data[lat][lng][pnu][self.code_translator.translate(
                            api_type, each_key)] = each_val
        file_path = "{}/../data/bldg_data".format(os.path.dirname(__file__))
        dist_file_path = self._createDir(file_path+"/dist")
        for lat, lat_data in giant_data.items():
            self._createDir(dist_file_path+"/"+lat)
            for lng, lng_data in lat_data.items():
                data_list = []
                for val in lng_data.values():
                    data_list.append(val)
                with open("{}/{}/{}.json".format(dist_file_path, lat, lng), "w", encoding="utf-8") as f:
                    json.dump(data_list, f, indent=4, ensure_ascii=False)

    def createDBType(self, service_name):
        distribution_data = self._saveLatLngCodeData(service_name)
        giant_data = {}
        key_list = []
        file_list = os.listdir(
            "{}/../data/bldg_data/raw/{}".format(os.path.dirname(__file__), service_name))
        for file_name in file_list:
            with open("{}/../data/bldg_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in data[0].keys():
                key_list.append(key)
            for each_data in data:
                pnu = each_data["NSDI:PNU"]
                latlng = distribution_data[pnu]
                lat, lng = latlng["lat_code"], latlng["lng_code"]
                if pnu not in giant_data.keys():
                    giant_data[pnu] = {"lat_code": lat, "lng_code": lng}
                for key, val in each_data.items():
                    giant_data[pnu][key] = val
        key_list = set(key_list)
        scheme = {}
        for key in key_list:
            if ("_PCLND" in key) or ("_code" in key):
                scheme[key] = "int"
            else:
                scheme[key] = "str"
        dict_list = {"scheme": scheme, "data": giant_data}
        with open("{}/../output/bldg_data_db_type.json".format(os.path.dirname(__file__)), "w", encoding="utf-8") as f:
            json.dump(dict_list, f, indent=4, ensure_ascii=False)

    def _getSeperatedPnuList(self, pnu_list):
        new_dict = {}
        for pnu in pnu_list:
            sigunguCd = pnu[0:5]
            bjdongCd = pnu[5:10]
            new_dict[sigunguCd + bjdongCd] = {
                "sigunguCd": sigunguCd, "bjdongCd": bjdongCd}
        return new_dict.values()

    def create(self, service_name_list):
        self._createDir(self.current_path+'/../data/bldg_data')
        self._createDir(self.current_path+'/../data/bldg_data/raw')
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
            self._distributeDataByLonLat(service)
        self.log("data successfully distributed")


if __name__ == "__main__":
    bldg_data_agent = BldgDataAgent()
    # print(land_data_agent.handleLandServiceConfigFromFile("pnu_list"))
    # bldg_data_agent.create(["TEST"])
    bldg_data_agent._distributeDataByLonLat("TEST")
    # land_data_agent.createDBType("GBD")
    # print(bldg_data_agent._getSeperatedPnu("1101202030"))
