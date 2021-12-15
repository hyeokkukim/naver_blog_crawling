# 파이썬으로 네이버 블로그 포스팅 크롤링

본 repository는 해당 [링크](https://yong0810.tistory.com/46)를 참고했습니다.

본 repository는 네이버 블로그 포스팅 데이터를 크롤링 하는 것으로 날짜, 기준을 설정해 데이터프레임에 저장하는 과정입니다.



____

해당 코드는 크롬 웹브라우저를 자동화해 네이버 블로그 포스팅 글을 크롤링 하는 것으로 본인 크롬 버전에 맞는 chromedriver를 다운받아야 합니다.

1. 크롬 버전 확인: 크롬 -> 설정 -> Chrome 정보 -> 버전 '96.0.4664.110'

   ![스크린샷 2021-12-15 오후 2.08.04](/Users/ranking/Library/Application Support/typora-user-images/스크린샷 2021-12-15 오후 2.08.04.png)

2. 크롬 드라이버 다운로드: [링크](https://chromedriver.chromium.org/downloads) 접속 후 버전에 맞는 드라이버 다운로드. 버전은 완전히 일치하지 않아도 되며 앞자리만 일치하면 됨

<img width="741" alt="스크린샷 2021-12-15 오후 2 06 13" src="https://user-images.githubusercontent.com/73429381/146127715-e8bba645-1ca7-4439-9320-b236424a4654.png">

_____



```python
import pandas as pd
import numpy as np
from selenium import webdriver
import time
from tqdm import tqdm





# 크롬 웹브라우저 실행

path = "/Users/ranking/OneDrive - UOS/0.Python_Coding/chromedriver" #chromedriver저장 경로(윈도우의 경우 chromedriver.exe)
driver = webdriver.Chrome(path)
url_list = []

#parameter
text = "동대문구" #검색어
start_date = '2021-01-01' #검색 시작일
end_date = '2021-12-31' #검색 종료일
order_by = 'sim' #정렬: 정확도순
#order_by = 'recentdate' #정렬: 최신순
page = 100 



for i in tqdm(range(1, page)):  # 1~page까지 크롤링
    url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=' + str(i) + '&rangeType=PERIOD&orderBy='+order_by+'&startDate='+ start_date +'&endDate='+end_date+'&keyword=' + text
    driver.get(url)
    time.sleep(0.5)

    for j in range(1, 5): # 페이지별 크롤링 할 블로그 개수 설정
        titles = driver.find_element_by_xpath('/html/body/ui-view/div/main/div/div/section/div[2]/div['+str(j)+']/div/div[1]/div[1]/a[1]')
        title = titles.get_attribute('href')
        url_list.append(title)

dict = {}
print("url 수집 끝, 해당 url 데이터 크롤링")

for url in tqdm(url_list): # 수집한 url 만큼 반복
    driver.get(url) # 해당 url로 이동
    driver.switch_to.frame('mainFrame')
    overlays = ".se-component.se-text.se-l-default" # 내용 크롤링
    contents = driver.find_elements_by_css_selector(overlays)    
    content_list = []

    for content in contents:
        content_list.append(content.text)
        content_str = ' '.join(content_list)
        dict[url] = content_str

print('contents 수집 끝')

crawling = pd.DataFrame.from_dict(dict,'index',columns = ['content'])
crawling['content'] = crawling['content'].str.replace('\n',' ')

crawling.to_csv('2021 크롤링 결과.csv')
crawling
```





|                                           content |                                                              |
| ------------------------------------------------: | ------------------------------------------------------------ |
|      https://blog.naver.com/wowhowow/222584028054 | 날이 정말 많이 추워졌는데요 그렇다보니 움직이기 귀찮은 게 있더라구요. 이런 추운 ... |
|       https://blog.naver.com/mun1453/222581046103 | 사람도 시간이 지나면 점점 노화가 찾아오듯이 집 또한 노화가 들면서 이곳저곳 손봐... |
|      https://blog.naver.com/minjii13/222580967366 | 안녕하세요 :3 사고르입니다아 카페 데이트 후 저녁밥 뭐먹을까 하다가 동대문구맛집 ... |
|  https://blog.naver.com/creation7881/222578879223 | 오늘은 서울 동대문구에 전농동에 위치한 전농sk아파트 32평아파트 시공사례입니다. ... |
|     https://blog.naver.com/5547sktlg/222585054480 | 오늘은 서울시 동대문구 전농동 295-501 그동안 선보인적 없는 복층형 오피스텔로... |
|                                               ... | ...                                                          |
|        https://blog.naver.com/uc0708/222410838770 | #대국꽃다발 #흰국화 #산소꽃다발 #대국 그리운 분께 인사가시면서 대국꽃다발을 주문... |
|     https://blog.naver.com/baksa8900/222592824720 | 안녕하세요! 부동산박사입니다 ~ ^^ 지난 11월 29일부터 운행을 시작한 2416... |
|  https://blog.naver.com/kkomange1818/222466058192 | 안녕하세요??^^ 1인 가구의 증가로 요새 오피스텔 전세가 품귀현상을 보이고 있는데... |
| https://blog.naver.com/handponmart77/222595345097 | 성동구, 동대문구, 중랑구 핸드폰 성지에서 휴대폰을 싸게 구입하는 방법을 알아보겠습... |
|    https://blog.naver.com/melgibshin/222351756086 | 안녕하세여 신축빌라를 소개하는 빌라쟁이 신팀장입니다 주말은 주말내내 비예보로 비... |

