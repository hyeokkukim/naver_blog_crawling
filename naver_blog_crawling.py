#link: https://yong0810.tistory.com/46
import pandas as pd
import numpy as np
from selenium import webdriver
import time
from tqdm import tqdm



# 크롬 웹브라우저 실행
path = "/Users/ranking/OneDrive - UOS/0.Python_Coding/chromedriver"
#path = '/Users/김혁구/Downloads/chromedriver_win32/chromedriver.exe' 
driver = webdriver.Chrome(path)
url_list = []

#parameter
text = "동대문구" #검색어
start_date = '2021-01-01' #검색 시작일
end_date = '2021-12-31' #검색 종료일
order_by = 'sim' #정렬: 정확도순
#order_by = 'recentdate' #정렬: 최신순
page = 100 #



for i in tqdm(range(1, page)):  # 1~page까지 크롤링
    #url = 'https://section.blog.naver.com/Search/Post.nhn?pageNo='+ str(i) + '&rangeType=ALL&orderBy=recentdate&keyword=' + text
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

