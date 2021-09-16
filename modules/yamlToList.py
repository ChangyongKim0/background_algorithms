import json
from collections import OrderedDict
import ruamel.yaml

yaml = ruamel.yaml.YAML()  # this uses the new API

# input_path = 'input/sample.yaml'
# output_path = 'output/sample.json'

yaml.indent(sequence=4, offset=2)

def setPath(file_type, file_name, file_name_out = -1):
    input_path = 'input/{}.yaml'.format(file_name)
    if file_name_out == -1:
        file_name_out = file_name
    output_path = 'output/{}.{}'.format(file_name_out, file_type)
    return input_path, output_path

def yamlToJson(file_name, file_name_out = -1):
    input_path, output_path = setPath('json', file_name, file_name_out)
    with open(input_path, 'r', encoding='UTF8') as stream:
        datamap = yaml.load(stream)
        with open(output_path, 'w') as output:
            json.dump(datamap, output, indent = 4, ensure_ascii=False)
    # return datamap

def yamlToList(file_name, file_name_out = -1, seperator = [' ', '-']):
    input_path, output_path = setPath('json', file_name, file_name_out)
    with open(input_path, 'r', encoding='UTF8') as stream:
        datamap = yaml.load(stream)
        k = json.loads(json.dumps(datamap, indent = 4, ensure_ascii=False))
        data_list = dictToList(k, seperator)
    return data_list


def dictToList(data, seperator = [' ', '-'], ignorer = '0'):
    new_seperator = [*seperator]
    each_seperator = seperator[0]
    if len(new_seperator) > 1:
        del new_seperator[0]

    if type(data) == dict and type(data) != int:
        data_list = []
        for each_key, each_val in data.items():
            if type(each_key) == int:
                each_key = str(each_key)
            data_sub_list = []
            for each_data in dictToList(each_val, new_seperator):
                if each_data == '0':
                    data_sub_list.append(each_key)
                else:
                    data_sub_list.append(each_key+each_seperator+each_data)
            data_list.extend(data_sub_list)
    elif type(data) == list:
        data_list = []
        for each_data in data:
            data_list.extend(dictToList(each_data, seperator))

    else:
        if type(data) == int:
            return [str(data)]
        else:
            return [data]
    return data_list


data_list = yamlToList('sample2')
for e in data_list:
    print(e)
# data = OrderedDict([('b', {'d': OrderedDict([('a', 1), ('c', 2)])})])
# data2 = OrderedDict([('논현동', [OrderedDict([(58, [0, 1, 2, 14, 3, 4, 10, 11, 12, 15, 3, 4, 10, 11, 12, 15, 5, 6, 7, 8, 9, 13])]), OrderedDict([(87, [0, 1, 2, 3, 4, 5, 7, 8])]), OrderedDict([(88, [0, 1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 17])]), OrderedDict([(128, [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 14])]), OrderedDict([(129, [0, 1, 2, 3, 7, 4, 5, 6, 8, 9])]), 
# OrderedDict([(207, [0, 4, 6, 1, 2, 3])]), OrderedDict([(208, [0, 1, 2, 5, 6, 7, 8, 15, 9, 13, 14])])])])
# print(data)
# print(dictToList(data2))
