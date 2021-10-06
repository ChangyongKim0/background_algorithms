import os
import json
import math

sigungu_code_path = "{}/../configs/sigungu_code.json".format(
    os.path.dirname(__file__))


class LatLngCodeGenerator:
    def __init__(self, service_name, echo=True, echo_error=True):
        self.echo = echo
        self.echo_error = echo_error
        self.distribution_data = self._saveLatLngCodeData(service_name)
        self.log("LatLngCodeGenerator of {} is loaded.".format(service_name))

    def log(self, content):
        if self.echo:
            print('LatLngGenerator> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('LatLngGenerator> \033[91m{}'.format(content) + '\033[0m')

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

    def get(self, pnu):
        if pnu in self.distribution_data.keys():
            return self.distribution_data[pnu]
        else:
            self.errlog("pnu value {} is not in data.".format(pnu))
            return -1

    def getLatCode(self, pnu):
        latlng = self.get(pnu)
        if latlng != -1:
            return latlng["lat_code"]
        else:
            return -1

    def getLngCode(self, pnu):
        latlng = self.get(pnu)
        if latlng != -1:
            return latlng["lng_code"]
        else:
            return -1


if __name__ == "__main__":
    code_gen_CBD = LatLngCodeGenerator("CBD")
    print(code_gen_CBD.get("1165010800113030037"))
    print(code_gen_CBD.getLatCode("1165010800113030037"))
    print(code_gen_CBD.getLngCode("1165010800113030037"))
    print(code_gen_CBD.get("11650100113030037"))
