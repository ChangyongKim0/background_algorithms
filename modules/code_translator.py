import os
import json

sigungu_code_path = "{}/../configs/translator_preset.json".format(
    os.path.dirname(__file__))


class CodeTranslator:
    def __init__(self, echo=True, echo_error=True):
        self.echo = echo
        self.echo_error = echo_error
        with open(sigungu_code_path, "r", encoding="utf-8") as json_file:
            self.translator = json.load(json_file)
        self.log("translator preset is loaded.")

    def log(self, content):
        if self.echo:
            print('CodeTranslator> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('CodeTranslator> \033[91m{}'.format(content) + '\033[0m')

    def translate(self, key, sub_key):
        if key in self.translator.keys():
            if sub_key in self.translator[key].keys():
                return self.translator[key][sub_key]
        self.errlog("No matching key in translator.")
        return -1

if __name__ == "__main__":
    code_translator = CodeTranslator()
    print(code_translator.translate("land_price", "NSDI:PSTYR_2_PBLNTF_PCLND"))
    print(code_translator.translate("land_price", "NSDI:PSTYR_1_PBLNTF_PCLND"))
    print(code_translator.translate("land_price", "NSDI:PSTYR_0_PBLNTF_PCLND"))
