from os import truncate
from urllib import request, parse
import requests
#  urlopen, urlencode, quote_plus
import json
import xmltodict
import datetime

class ApiRequester:
    def __init__(self, authkey_path, authkey_type, base_url_path):
        self.urllist = []
        self.type = authkey_type
        with open(base_url_path, "r") as json_file:
            key_list = json.load(json_file)
            self.base_url = key_list[authkey_type]
        with open(authkey_path, "r") as json_file:
            key_list = json.load(json_file)
            self.authkey = key_list[authkey_type]
        self.log('authorization key is set successfully.')

    def log(self, content):
        print('getAPI_{}> {}'.format(self.type, content))

    def loadInput(self, input_path):
        with open(input_path, "r") as json_file:
            input = json.load(json_file)
            self.setInputs(input['input_base'], input['list_key'], input['list_val'])

    def setInput(self, input, is_direct = True):
        new_dict = {}
        for key, val in input.items():
            new_dict[parse.quote_plus(key)] = val
        self.urllist.append('{}?authkey={}&format=xml&{}'.format(self.base_url, self.authkey, parse.urlencode(new_dict)))
        if is_direct:
            self.log('input link appended successfully.')

    def setInputs(self, input_base, list_key, list_val):
        is_direct = False
        for val in list_val:
            input_copy = {**input_base}
            input_copy[list_key] = val
            self.setInput(input_copy, is_direct)
        self.log('input links appended successfully.')

    def setOutputName(self, path, name):
        self.save_name = '{}/{}.json'.format(path, name)
        self.save_name_raw = '{}/{}_raw.json'.format(path, name)
    
    def getInputs(self):
        for url in self.urllist:
            self.log(url)
        self.log('got all input links successfully: total {} inputs.'.format(len(self.urllist)))

    def _requestOuputs(self):
        output = []
        for url in self.urllist:
            req = request.Request(url)
            req.get_method = lambda: 'GET'
            req_dict = json.loads(json.dumps(xmltodict.parse(request.urlopen(req).read()), indent=4, ensure_ascii=False))
            output.append(req_dict)
        self.log('got all requested data successfully.')
        return output

    def _dictExtractorByKeys(self, data, keys, is_parent = True):
        if is_parent == True:
            data_list = []
            for each_data in data:
                data_list.extend(self._dictExtractorByKeys(each_data, keys, False)['vals'])
        else:
            key_data_list = []
            val_data_list = []
            for key in keys:
                key_val, key_path = self._findkeyPath(data, key)
                self.log('Found path of [{}]: [{}]'.format(key, ' -> '.join(key_path)))
                key_data_list.append({'val': key_val, 'path': key_path})
            for key_data in key_data_list:
                if key_data['val']:
                   val_data_list.append(self._getValByPath(data, key_data['path']))
            data_list = self._flipList(val_data_list)
        return {'keys': keys, 'vals': data_list}
        

    def _flipList(self, data):
        print(data)
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
                    val=True
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


    def getOutputs(self, keys = -1, output_type='json'): # or csv
        if keys == -1:
            data_converted = self._requestOuputs()
            with open(self.save_name_raw, "w") as json_file:
                    json.dump(data_converted, json_file, indent = 4, ensure_ascii=False)
        else:
            output = self._requestOuputs()
            data = self._dictExtractorByKeys(output, keys)
            if output_type == 'json':
                data_converted = self._toJson(data)
                with open(self.save_name, "w") as json_file:
                    json.dump(data_converted, json_file, indent = 4, ensure_ascii=False)
        self.log('file successfully written.')
        

if __name__ == '__main__':
    base_url = "http://openapi.nsdi.go.kr/nsdi/LandUseService/wfs/getLandUseWFS"
    authkey_path = 'security/authkey.json'
    authkey_type = 'WFS'
    input_dict = {
        # 'bbox': '217365,447511,217636,447701,EPSG:5174',
        'maxFeatures': '10',
        'resultType': 'results',
        'srsName': 'EPSG:5174'
    }
    pnu_list = ['4145011800100320003', '4145011800100320003']
    get_api = ApiRequester(authkey_path, authkey_type, base_url)
    get_api.setInput(input_dict)
    get_api.setInputs(input_dict, 'pnu', pnu_list)
    get_api.setOutputName('.', 'tempfile2')
    get_api.getInputs()
    get_api.getOuputs()
    sample_data = {'f': {'e':[{'a':{'c':1, 'd':2}, 'b':3}, {'a':{'c':4, 'd':5}, 'b':6}, {'a':{'c':7, 'd':8}, 'b':9}], 'f':[{'aa':{'cc':3, 'dc':4}, 'bb':2}, {'aa':{'cc':6, 'dd':7}, 'bc':5}, {'aa':{'cc':9, 'dd':10}, 'bb':8}]}}
    print(get_api._toJson(get_api._dictExtractorByKeys(sample_data, ['a', 'b'])))
    keys_request = ["NSDI:PNU",
                    "NSDI:LD_CPSG_CODE",
                    "NSDI:LD_EMD_LI_CODE",
                    "NSDI:REGSTR_SE_CODE",
                    "NSDI:MNNM"]
    get_api.getOutputs(keys_request)


