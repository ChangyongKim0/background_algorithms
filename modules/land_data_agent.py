import os
import datetime
import json
import api_agent


class LandDataAgent:
    # def __init__(self):
    #     api_requester = ApiRequester()

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
                print("Error: the service already exist. Create after delete it.")
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

    def create(self, service_name_list):
        get_api = api_agent.ApiAgent("land")
        config_data = self._getConfig("land_service")
        input_list = []
        for service in service_name_list:
            for key, val in config_data[service]["organized_pnu_list"].items():
                input_list.append({"pnu": key, "filter_output": val})
            get_api.getApi(
                "{}/../data/land_data/raw/{}".format(os.path.dirname(__file__), service), input_list)


if __name__ == "__main__":
    land_data_agent = LandDataAgent()
    # print(land_data_agent.handleLandServiceConfigFromFile("pnu_list"))
    land_data_agent.create(["GBD"])
