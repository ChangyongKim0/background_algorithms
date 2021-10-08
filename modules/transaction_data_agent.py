# 주거는 pnu 있음
# officetel_rent
# officetel_trade
# apt_right

# apt_rent
# apt_trade
# rh_rent
# th_trade

# pnu 가능성 -> 강욱이형한테
# nrg_trade
import os
import datetime
import json
import api_agent
import math
import code_translator
import identification_number_generator
import lat_lng_code_generator


class TransactionDataAgent:
    def __init__(self, echo=True, echo_error=True):
        self.get_api = api_agent.ApiAgent("transaction")
        self.get_api_deep = api_agent.ApiAgent("transaction_need_analysis")
        self.code_translator = code_translator.CodeTranslator()
        self.id_generator = identification_number_generator.IdentificationNumberGenerator()
        self.echo = echo
        self.echo_error = echo_error
        self.current_path = os.path.dirname(__file__)

    def log(self, content):
        if self.echo:
            print('TransactionDataAgent> \033[92m{}'.format(
                content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('TransactionDataAgent> \033[91m{}'.format(
                content) + '\033[0m')

    def importantLog(self, content, echo=-1):
        prev_echo = self.echo
        self.echo = True
        self.log(content)
        if echo == -1:
            self.echo = prev_echo
        else:
            self.echo = echo

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

    def _createTransactionDataTree(self, service_name, dir_list):
        giant_data = {}
        code_gen = lat_lng_code_generator.LatLngCodeGenerator(service_name)
        for dir_name in dir_list:
            file_list = os.listdir(
                "{}/../data/transaction_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, dir_name))
            for file_name in file_list:
                self.log("distribute data in file {}".format(file_name))
                api_type = file_name.split(".")[0]
                with open("{}/../data/transaction_data/raw/{}/{}/{}".format(os.path.dirname(__file__), service_name, dir_name, file_name), "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.log("raw data length is {}.".format(len(data)))
                for each_data in data:
                    id_data = self.id_generator.convert(api_type, each_data)
                    # self.log(id_data)
                    pnu = id_data["id"]
                    count = id_data["id_count"]
                    latlng = code_gen.get(pnu)
                    if latlng == -1:
                        continue
                    lat, lng = latlng["lat_code"], latlng["lng_code"]
                    if lat not in giant_data.keys():
                        giant_data[lat] = {}
                    if lng not in giant_data[lat].keys():
                        giant_data[lat][lng] = {}
                    if pnu not in giant_data[lat][lng].keys():
                        giant_data[lat][lng][pnu] = {
                            "id": pnu, "service_name": service_name, "transaction_list": {}}
                    if count > 1 and id_data["id_2"] not in giant_data[lat][lng][pnu]["transaction_list"].keys():
                        giant_data[lat][lng][pnu]["transaction_list"][id_data["id_2"]] = {
                            "id": id_data["id_2"], "estate_list": {}}
                    if count > 2 and id_data["id_3"] not in giant_data[lat][lng][pnu]["transaction_list"][id_data["id_2"]]["estate_list"].keys():
                        giant_data[lat][lng][pnu]["transaction_list"][id_data["id_2"]]["estate_list"][id_data["id_3"]] = {
                            "id": id_data["id_3"]}
                    for each_key, each_val in each_data.items():
                        if count == 1:
                            giant_data[lat][lng][pnu][self.code_translator.translate(
                                api_type, each_key)] = each_val
                        elif count == 2:
                            giant_data[lat][lng][pnu]["transaction_list"][id_data["id_2"]][self.code_translator.translate(
                                api_type, each_key)] = each_val
                        elif count == 3:
                            giant_data[lat][lng][pnu]["transaction_list"][id_data["id_2"]]["estate_list"][id_data["id_3"]][self.code_translator.translate(
                                api_type, each_key)] = each_val
                self.importantLog(
                    "distribution of file {} finished.".format(file_name))
            self.importantLog(
                "distribution of dir {} finished.".format(dir_name))

    def distributeDataByLonLat(self, service_name):
        dir_list = os.listdir(
            "{}/../data/transaction_data/raw/{}".format(os.path.dirname(__file__), service_name))
        giant_data = self._createTransactionDataTree(service_name, dir_list)
        file_path = "{}/../data/transaction_data".format(
            os.path.dirname(__file__))
        dist_file_path = self._createDir(file_path+"/dist")
        for lat, lat_data in giant_data.items():
            self._createDir(dist_file_path+"/"+lat)
            for lng, lng_data in lat_data.items():
                pnu_list = []
                for pnu_data in lng_data.values():
                    transaction_list = []
                    for transaction_data in pnu_data["transaction_list"].values():
                        estate_list = []
                        for estate_data in transaction_data["estate_list"].values():
                            estate_list.append(estate_data)
                        transaction_data["estate_list"] = estate_list
                        transaction_list.append(transaction_data)
                    pnu_data["transaction_list"] = transaction_list
                    pnu_list.append(pnu_data)
                with open("{}/{}/{}.json".format(dist_file_path, lat, lng), "w", encoding="utf-8") as f:
                    json.dump(pnu_list, f, indent=4, ensure_ascii=False)

    def createDBType(self, service_name):
        distribution_data = self._saveLatLngCodeData(service_name)
        giant_data = {}
        key_list = []
        file_list = os.listdir(
            "{}/../data/transaction_data/raw/{}".format(os.path.dirname(__file__), service_name))
        for file_name in file_list:
            with open("{}/../data/transaction_data/raw/{}/{}".format(os.path.dirname(__file__), service_name, file_name), "r", encoding="utf-8") as f:
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
        with open("{}/../output/transaction_data_db_type.json".format(os.path.dirname(__file__)), "w", encoding="utf-8") as f:
            json.dump(dict_list, f, indent=4, ensure_ascii=False)

    def _getSeperatedPnuList(self, pnu_list):
        new_dict = {}
        for pnu in pnu_list:
            sigunguCd = pnu[0:5]
            new_dict[sigunguCd] = {
                "sigunguCd": sigunguCd}
        return new_dict.values()

    def createMonthData(self, service, deal_ymd):
        self._createDir(self.current_path+'/../data/transaction_data')
        self._createDir(self.current_path+'/../data/transaction_data/raw')
        config_data = self._getConfig("land_service")
        input_list = []
        input_list_seperated = []
        sep_key_list = self._getSeperatedPnuList(
            config_data[service]["organized_pnu_list"].keys())
        for sep_key in sep_key_list:
            input_list.append(
                {"LAWD_CD": sep_key["sigunguCd"], "DEAL_YMD": deal_ymd})
        # self.log(input_list)
        # self.log(input_list_seperated)
        self._createDir(self.current_path +
                        '/../data/transaction_data/raw/{}'.format(service))
        self._createDir(self.current_path +
                        '/../data/transaction_data/raw/{}/{}'.format(service, deal_ymd))
        self.get_api.getApi(
            self.current_path+'/../data/transaction_data/raw/{}/{}'.format(service, deal_ymd), input_list)
        # self.get_api_deep.getApi(
        #     self.current_path+'/../data/transaction_data/raw/{}/{}'.format(service, deal_ymd), input_list)

    def _nextYMD(self, ymd):
        year = ymd[0:4]
        month_int = int(ymd[4:6])
        if month_int < 9:
            return year + '0' + str(month_int + 1)
        elif month_int < 12:
            return year + str(month_int + 1)
        else:
            return str(int(year)+1) + '01'

    def create(self, service_name_list, deal_ymd_start, deal_ymd_end, echo=True):
        self.echo = echo
        if int(deal_ymd_end) <= int(deal_ymd_start) or int(deal_ymd_end[4:6]) > 12:
            self.errlog("wrong inputs.")
            return -1
        deal_ymd = deal_ymd_start
        while deal_ymd != deal_ymd_end:
            for service in service_name_list:
                self.createMonthData(service, deal_ymd)
            self.importantLog("{} data at ymd {} created successfully.".format(
                service, deal_ymd), echo)
            deal_ymd = self._nextYMD(deal_ymd)

        # self.distributeDataByLonLatFullData()
        self.importantLog("data distributed successfully.", echo)


if __name__ == "__main__":
    transaction_data_agent = TransactionDataAgent()
    # print(land_data_agent.handleLandServiceConfigFromFile("pnu_list"))
    # transaction_data_agent.create(
    #     ["CBD", "YBD", "GBD"], '200101', '201412', echo=False)
    transaction_data_agent.distributeDataByLonLat("TEST")
    # land_data_agent.createDBType("GBD")
    # print(transaction_data_agent._getSeperatedPnu("1101202030"))
