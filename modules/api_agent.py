import os
from urllib import request, parse
import json
import xmltodict

config_path = "{}/../configs/api_preset.json".format(os.path.dirname(__file__))
authkey_path = "{}/../security/authkey.json".format(os.path.dirname(__file__))


class ApiAgent:
    def __init__(self, type, echo=True, echo_error=True):
        self.urllist = []
        self.filter_list = []
        self.type = type
        self.echo = echo
        self.echo_error = echo_error
        with open(config_path, "r") as json_file:
            self.api_preset = json.load(json_file)
        with open(authkey_path, "r") as json_file:
            self.authkey = json.load(json_file)
        self.log(
            'configuration preset and authorization key is set successfully.' + '\033[0m')

    def log(self, content):
        if self.echo:
            print('ApiAgent {}> \033[92m{}'.format(
                self.type, content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('ApiAgent {}> \033[91m{}'.format(
                self.type, content) + '\033[0m')

    # def loadInput(self, input_path):
    #     with open(input_path, "r") as json_file:
    #         input = json.load(json_file)
    #         self.setInputs(input['input_base'], input['list_key'], input['list_val'])

    def setInput(self, api_type, input, is_direct=True):
        self.api_type = api_type
        new_dict = {}
        preset = self.api_preset["api_key_list"][api_type]
        for key, val in preset["base_inputs"].items():
            new_dict[parse.quote_plus(key)] = val
        if len(preset["required_input_list"]) > 0:
            for key in preset["required_input_list"]:
                new_dict[parse.quote_plus(key)] = input[key]
        self.urllist.append('{}?{}={}&format=xml&{}'.format(
            preset["base_url"], preset["authkey_name"], self.authkey[api_type], parse.urlencode(new_dict)))
        if len(preset["filter_output"]) > 0:
            self.filter_list.append(input["filter_output"])
        else:
            self.filter_list.append(-1)
        if is_direct:
            self.log('input link appended successfully.')

    def setInputs(self, api_type, input_list):
        self.api_type = api_type
        is_direct = False
        for input in input_list:
            self.setInput(api_type, input, is_direct)
        self.log('input links appended successfully.')

    def setOutputName(self, path, name):
        self.save_name = '{}/{}.json'.format(path, name)

    def getInputs(self, important=False):
        for url in self.urllist:
            if important:
                self.errlog(url)
            else:
                self.log(url)
        self.log('got all input links successfully: total {} inputs.'.format(
            len(self.urllist)))

    def _requestOuputs(self):
        output = []
        for url in self.urllist:
            req = request.Request(url)
            req.get_method = lambda: 'GET'
            req_dict = json.loads(json.dumps(xmltodict.parse(
                request.urlopen(req).read()), indent=4, ensure_ascii=False))
            output.append(req_dict)
        self.log('got all requested data successfully.')

        try:
            self.errlog(output[0]['response']['resultMsg'])
            self._throwUrlError()
        except:
            try:
                self.errlog(output[0]['ows:ExceptionReport']
                            ['ows:Exception']['ows:ExceptionText'])
                self._throwUrlError()
            except:
                -1
        return output

    def _throwUrlError(self):
        self.errlog("please refer the url below.")
        self.getInputs(important=True)
        self.errlog("url end.")

    def _dictExtractorByKeys(self, data, keys, is_parent=True):
        if is_parent == True:
            data_list = []
            for each_data in data:
                data_list.append(self._dictExtractorByKeys(
                    each_data, keys, False)['vals'])
        else:
            key_data_list = []
            val_data_list = []
            for key in keys:
                key_val, key_path = self._findkeyPath(data, key)
                if key_val:
                    self.log('Found path of [{}]: [{}]'.format(
                        key, ' -> '.join(key_path)))
                else:
                    self.errlog('Cannot find path of {}.'.format(key))
                key_data_list.append({'val': key_val, 'path': key_path})
            for key_data in key_data_list:
                if key_data['val']:
                    val_data_list.append(
                        self._getValByPath(data, key_data['path']))
            data_list = self._flipList(val_data_list)
        return {'keys': keys, 'vals': data_list}

    def _flipList(self, data):
        if len(data) == 0:
            return data
        if type(data[0]) != list:
            return [data]
        else:
            data_flipped = []
            for i in range(len(data[0])):
                temp_data = []
                for j in range(len(data)):
                    temp_data.append(data[j][i])
                data_flipped.append(temp_data)
            return data_flipped

    def _getValByPath(self, data, path_old):
        path = [*path_old]
        try:
            if len(path) != 1:
                if type(data) == list:
                    val = []
                    del path[0]
                    for i in range(len(data)):
                        val.append(self._getValByPath(data[i], path))
                else:
                    key = path.pop(0)
                    val = self._getValByPath(data[key], path)
            else:
                val = data[path[0]]
            # print(val)
            return val
        except:
            return -1

    def _findkeyPath(self, data, key):
        val = False
        if type(data) == list:
            for each_data in data:
                # print(each_data)
                sub_val, path = self._findkeyPath(each_data, key)
                if sub_val:
                    val = True
                    path.insert(0, '<list>')
                    break
        else:
            try:
                if key in data.keys():
                    return True, [key]
                else:
                    for sub_key, sub_data in data.items():
                        sub_val, path = self._findkeyPath(sub_data, key)
                        if sub_val:
                            val = True
                            path.insert(0, sub_key)
                            break
            except:
                return False, -1
        if val:
            return True, path
        else:
            return False, -1

    def _toJson(self, data):
        # print(data)
        keys = data['keys']
        vals = data['vals']
        dict_list = []
        for row in vals:
            temp_dict = {}
            for i, key in enumerate(keys):
                temp_dict[key] = row[i]
            dict_list.append(temp_dict)
        return dict_list

    def _filterByKey(self, output, key):
        new_vals = []
        filter_index = output["keys"].index(key)
        for i, bundle in enumerate(output['vals']):
            if self.filter_list[i] == -1:
                new_bundle = bundle
            else:
                new_bundle = []
                for ele in bundle:
                    if ele[filter_index] in self.filter_list[i]:
                        new_bundle.append(ele)
            new_vals.extend(new_bundle)
        return {"keys": output["keys"], "vals": new_vals}

    def _flattener(self, output):
        new_vals = []
        for bundle in output["vals"]:
            new_vals.extend(bundle)
        return {"keys": output["keys"], "vals": new_vals}

    def getOutputs(self, output_type='json'):  # or csv
        keys = self.api_preset["api_key_list"][self.api_type]["required_output_list"]
        filter_keys = self.api_preset["api_key_list"][self.api_type]["filter_output"]
        output = self._requestOuputs()
        data_temp = self._dictExtractorByKeys(output, keys)
        if len(filter_keys) == 0:
            data = self._flattener(data_temp)
        else:
            data = self._filterByKey(data_temp, filter_keys[0])
        if output_type == 'json':
            data_converted = self._toJson(data)
            with open(self.save_name, "w", encoding='utf-8') as json_file:
                json.dump(data_converted, json_file,
                          indent=4, ensure_ascii=False)
        self.log('file successfully written.')
        if len(data_converted) == 0:
            self.errlog("but there is no data.")
            self._throwUrlError()
        self.urllist = []

    def getApi(self, output_path, input_list):
        api_list = self.api_preset["api_list_to_request"][self.type]
        for api_type in api_list:
            self.setInputs(api_type, input_list)
            self.setOutputName(output_path, api_type)
            self.getOutputs()
        return api_list

    def getRawOutputs(self):
        output = self._requestOuputs()
        with open(self.save_name, "w", encoding='utf-8') as json_file:
            json.dump(output, json_file,
                      indent=4, ensure_ascii=False)
        self.log('file successfully written.')
        if len(output) == 0:
            self.errlog("but there is no data.")
            self._throwUrlError()
        self.urllist = []

    def getRawApi(self, output_path, input_list):
        api_list = self.api_preset["api_list_to_request"][self.type]
        for api_type in api_list:
            self.setInputs(api_type, input_list)
            self.setOutputName(output_path, api_type)
            self.getRawOutputs()
        return api_list


if __name__ == '__main__':
    input_dict = {
        # 'bbox': '217365,447511,217636,447701,EPSG:5174',
        'maxFeatures': '10',
        'resultType': 'results',
        'srsName': 'EPSG:5174'
    }
    pnu_list = ['4145011800100320003', '4145011800100320003']
    get_api = ApiAgent("land")
    sample_data = [{'f': {'e': [{'a': {'c': 1, 'd': 2}, 'b': 3}, {'a': {'c': 4, 'd': 5}, 'b': 6}, {'a': {'c': 7, 'd': 8}, 'b': 9}], 'f': [
        {'aa': {'cc': 3, 'dc': 4}, 'bb': 2}, {'aa': {'cc': 6, 'dd': 7}, 'bc': 5}, {'aa': {'cc': 9, 'dd': 10}, 'bb': 8}]}}]
    print(get_api._toJson(
        get_api._dictExtractorByKeys(sample_data, ['a', 'b'])))
    get_api.getApi("{}/../output/land_data_sample".format(os.path.dirname(__file__)), [{"pnu": "116801050010111011", "filter_output": ["1168010500101110114"]}, {
        "pnu": "116801050010112000", "filter_output": ["1168010500101120001"]}])
    get_api.getRawApi("{}/../output/land_data_raw_sample".format(os.path.dirname(__file__)), [{"pnu": "116801050010111011", "filter_output": ["1168010500101110114"]}, {
        "pnu": "116801050010112000", "filter_output": ["1168010500101120001"]}])
