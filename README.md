# 파일 동기화하기

1. 터미널 열기

1. 원하는 폴더로 이동.

   ```
   cd 원하는_폴더
   ```

1. 터미널 창에 다음을 입력

   ```terminal
   git clone https://github.com/ChangyongKim0/background_algorithms.git
   ```

# 파일 및 폴더 세팅

> configs
>
> > 설정 파일들이 위치함

> data
>
> > 데이터가 쌓여지는 공간.  
> > 현재 `land_data/raw/GBD` 안에 raw data 위치

> input
>
> > 인풋을 넣어두는 곳.  
> > `pnu_list.txt` 한번 확인하면 좋음.

> modules
>
> > 필요한 알고리즘들이 들어 있는 폴더.

> > `api_agent.py:` api 가져오는 내부 코드

> > `api_requester.py:` 일반 테스트용 api 가져오는 코드

> > `land_data_agent.py:` 토지 데이터 저장하는 코드

> > `logger.py:` 고급 로거를 만들려고 생각중.. 아직 작성안함.

> > `yamlToList.py:` yaml 파일을 list로 바꾸어주는 코드

> **output**
>
> > **만들어야 하는 폴더!!**  
> > db에 쌓을 필요 없는 출력 데이터 저장용.

> **security**
>
> > **만들어야 하는 폴더!!**

> > `authkey.json`
> >
> > > **만들어야 하는 파일!!**  
> > > 아래와 같은 형식으로 작성

```json
{
  "API 타입": "키값",
  "land_use_WFS": "XXXXXX",
  "land_use_WMS": "XXXXXX"
}
```

> > > API 타입은 `configs/api_preset.json`에 있는 것과 동일해야 함.
