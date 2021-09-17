import api_requester

# 요청종류 세팅
authkey_path = 'security/authkey.json'
base_url_path = 'security/url.json'
authkey_type = 'char_WFS'

# 인풋, 요청 키 값 세팅(변수 이름이나 내부 내용은 자유롭게 변경해도 됩니다.)
input_dict = {
    # 'bbox': '217365,447511,217636,447701,EPSG:5174',
    'pnu': '1114010500',
    'maxFeatures': '100',
    'resultType': 'results',
    'srsName': 'EPSG:4326'
}
input_dict2 = {
    'maxFeatures': '10',
    'resultType': 'results',
    'srsName': 'EPSG:5174'
}
pnu_list = ['1111017400105950132', '4145011800100320003'] # 리스트 인풋이 필요한 경우
keys_request = ["NSDI:PNU",
                "gml:posList",
                "NSDI:LNM_LNDCGR_SMBOL",
                "NSDI:PBLNTF_PCLND"]

# ApiRequester 생성 - 수정 X
get_api = api_requester.ApiRequester(authkey_path, authkey_type, base_url_path)

# 인풋 넣기 (여러번 넣어도 됨.)
# get_api.setInput(input_dict) # 단순 인풋
get_api.setInput(input_dict) # 단순 인풋

# 아웃풋 파일 이름 설정
get_api.setOutputName('./output', 'junggu_sample') 

# ApiRequester 작동
# get_api.getOutputs() # 요청 키가 없는 경우 로우 파일이 생성됨.
get_api.getOutputs(keys_request) # 요청 키가 있는 경우 해당 키에 대한 정보만 받아옴.