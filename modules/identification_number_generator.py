import os
import json

sigungu_code_path = "{}/../configs/sigungu_code.json".format(
    os.path.dirname(__file__))

# id_count id id_2 id_3 ... 에 해당하는 값을 반환


class IdentificationNumberGenerator:
    def __init__(self, echo=True, echo_error=True):
        self.random_id = "0"
        self.echo = echo
        self.echo_error = echo_error
        with open(sigungu_code_path, "r", encoding="utf-8") as json_file:
            self.sigungu_code_list = json.load(json_file)
        self.log("sigungu code is loaded.")

    def _getNewRandomId(self):
        random_id =  self.random_id
        self.random_id = str(int(random_id) + 1)
        return random_id

    def log(self, content):
        if self.echo:
            print('IdNoGenerator> \033[92m{}'.format(content) + '\033[0m')

    def errlog(self, content):
        if self.echo_error:
            print('IdNoGenerator> \033[91m{}'.format(content) + '\033[0m')

    def _convertBJD(self, data):
        if " " in data:
            return self.sigungu_code_list["to_code"][data]
        else:
            return self.sigungu_code_list["from_code"][data]

    def _fillZero(self, data, length=4):
        zero_number = length - len(data)
        converted = ""
        for i in range(zero_number):
            converted += "0"
        converted += data
        return converted
    
    def _fillSpace(self, data):
        if data[0] == " ":
            return data
        data = ' ' + data
        return data

    def convert(self, type, data):
        if type in ["officetel_rent", "officetel_trade", "apt_right"]:
            if data["년"] == -1:
                return {"id_count": 3, "id": -1, "id_2": -1, "id_3": -1}
            try:
                jibun = data["지번"].split('-')
            except:
                print(type, data)
                jibun = data["지번"].split('-')
            if len(jibun) == 1:
                jibun_code = self._fillZero(jibun[0]) + "0000"
            else:
                jibun_code = self._fillZero(
                    jibun[0]) + self._fillZero(jibun[1])
            id = self._convertBJD("서울특별시 {}{}".format(
                data["시군구"], self._fillSpace(data["법정동"]))) + "1" + jibun_code
            id_2 = data['년'] + self._fillZero(data['월'],
                                              length=2), self._fillZero(data['일'], length=2)
            id_3 = self._getNewRandomId()
            return {"id_count": 3, "id": id, "id_2": id_2, "id_3": id_3}
        elif type in ["apt_rent", "apt_trade", "multiple_housing_rent", "multiple_housing_trade"]:
            if data["년"] == -1:
                return {"id_count": 3, "id": -1, "id_2": -1, "id_3": -1}
            gu_name = self._convertBJD(data["지역코드"]+"00000")
            jibun = data["지번"].split('-')
            if len(jibun) == 1:
                jibun_code = self._fillZero(jibun[0]) + "0000"
            else:
                jibun_code = self._fillZero(
                    jibun[0]) + self._fillZero(jibun[1])
            id = self._convertBJD("{}{}".format(
                gu_name, self._fillSpace(data["법정동"]))) + "1" + jibun_code
            id_2 = data['년'] + self._fillZero(data['월'],
                                              length=2), self._fillZero(data['일'], length=2)
            id_3 = self._getNewRandomId()
            return {"id_count": 3, "id": id, "id_2": id_2, "id_3": id_3}
        elif type == "multiple_housing_trade":
            return -1
        elif type == "land_trade":
            return -1
        elif type == "bldg_floor":
            if data["sigunguCd"] == -1:
                return {"id_type": "bldg", "id_count": 4, "id": "-1", "id_2": "-1", "id_3": "-1", "id_4": "-1"}
            if data["platGbCd"] == "0":
                temp = "1"
            else:
                temp = "0"
            id = data["sigunguCd"] + data["bjdongCd"] + \
                temp + data["bun"] + data["ji"]
            id_2 = data["mgmBldrgstPk"]
            id_3 = data["flrGbCd"] + data["flrNo"].split(".")[0]
            id_4 = data["rnum"]
            return {"id_type": "bldg", "id_count": 4, "id": id, "id_2": id_2, "id_3": id_3, "id_4": id_4}
            # 4개로
        elif type == "bldg_title":
            if data["sigunguCd"] == -1:
                return {"id_type": "bldg", "id_count": 2, "id": "-1", "id_2": "-1"}
            if data["platGbCd"] == "0":
                temp = "1"
            else:
                temp = "0"
            id = data["sigunguCd"] + data["bjdongCd"] + \
                temp + data["bun"] + data["ji"]
            id_2 = data["mgmBldrgstPk"]
            return {"id_type": "bldg", "id_count": 2, "id": id, "id_2": id_2}
        elif type == "bldg_year":
            if data["NSDI:PNU"] == -1:
                return {"id_type": "bldg", "id_count": 1, "id": "-1"}
            return {"id_type": "bldg", "id_count": 1, "id": data["NSDI:PNU"]}
        elif type == "bldg_title_total":
            if data["sigunguCd"] == -1:
                return {"id_type": "bldg", "id_count": 1, "id": "-1"}
            if data["platGbCd"] == "0":
                temp = "1"
            else:
                temp = "0"
            id = data["sigunguCd"] + data["bjdongCd"] + \
                temp + data["bun"] + data["ji"]
            return {"id_type": "bldg", "id_count": 1, "id": id}
        elif type == "bldg_connect":
            if data["sigunguCd"] == -1:
                return {"id_type": "pnu", "id_count": 2, "id": "-1", "id_2": "-1"}
            if data["platGbCd"] == "0":
                temp = "1"
            else:
                temp = "0"
            if data["atchPlatGbCd"] == "0":
                temp_2 = "1"
            else:
                temp_2 = "0"
            id = data["sigunguCd"] + data["bjdongCd"] + \
                temp + data["bun"] + data["ji"]
            try:
                id_2 = data["atchSigunguCd"] + data["atchBjdongCd"] + \
                    temp_2 + data["atchBun"] + data["atchJi"]
            except:
                return {"id_type": "pnu", "id_count": 2, "id": "-1", "id_2": "-1"}
            return {"id_type": "pnu", "id_count": 2, "id": id, "id_2": id_2}
        return -1


if __name__ == "__main__":
    idgen = IdentificationNumberGenerator()
    # print(idgen.sigungu_code_list)
    officetel_rent_data = {
        "거래금액": "9,500",
        "건축년도": "1998",
        "년": "2015",
        "단지": "파크뷰타워",
        "법정동": " 필운동",
        "시군구": "종로구",
        "월": "12",
        "일": "31",
        "전용면적": "24.3",
        "지번": "285-5",
        "지역코드": "11110",
        "층": "2",
        "해제사유발생일": " ",
        "해제여부": " "
    }
    apt_rent_data = {
        "건축년도": "2007",
        "년": "2015",
        "법정동": " 필운동",
        "보증금액": " 65,000",
        "아파트": "신동아블루아광화문의 꿈",
        "월": "12",
        "월세금액": " 0",
        "일": "4",
        "전용면적": "111.9",
        "지번": "254",
        "지역코드": "11110",
        "층": "7",
    }
    print(idgen.convert("officetel_rent", officetel_rent_data))
    print(idgen.convert("apt_rent", apt_rent_data))
