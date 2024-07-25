import requests
from bs4 import BeautifulSoup
import pandas as pd
# import schedule
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import time
from datetime import datetime

now = time.time()
dt = datetime.fromtimestamp(now)
dt_str = str(dt)[:10]

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

print(os.getcwd())

# 데이터 모델 정의
class Job(BaseModel):
    Title: str
    Company: str
    Location: str
    Date: str
    Exp: str
    Edu: str
    URL: str

# 웹 크롤링 및 엑셀 저장 함수 정의
def scrape_jobs_and_save_to_excel():
    print('크롤링 시작')

    # 스크래핑할 웹 사이트의 url을 선언, f-string을 이용해 page number를 바꾸어가며 탐색할 수 있도록 함.
    page_no = 1
    url = f'https://www.jobkorea.co.kr/Search/?stext=%ED%8C%8C%EC%9D%B4%EC%8D%AC&tabType=recruit&Page_No={page_no}'

    # DataFrame 선언
    df = pd.DataFrame( columns = ['공고명','회사명','직장 위치','마감 기한','채용 형태(경력, 신입)','공고 링크'])

    # 스크래핑할 웹 사이트의 총 페이지 수 파악
    # '총 OOOO건' 이라는 검색 결과를 스크래핑하여 한 페이지당 표시 수인 20으로 나누기
    response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    soup = BeautifulSoup(response.text,'html.parser')

    pages = soup.find('p','filter-text').find('strong').text.replace(',','')
    pages = round(int(pages)/20)

    for i in range(pages):
        # 웹 페이지 요청
        url = f'https://www.jobkorea.co.kr/Search/?stext=%ED%8C%8C%EC%9D%B4%EC%8D%AC&tabType=recruit&Page_No={i}'
        response = requests.get(url, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        response.raise_for_status()  # 요청이 성공했는지 확인

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        # 채용 공고 리스트 찾기
        titles = soup.find_all('a','name dev_view')
        urls = soup.find_all('a','name dev_view')
        companies = soup.find_all('a', 'title dev_view')
        locations = soup.find_all('span','loc long')
        dates = soup.find_all('span','date')
        experiences = soup.find_all('span','exp')
        educations = soup.find_all('span','edu')

        data = []
        # 각 채용 공고에서 필요한 데이터 추출
        for job in range(20):
            title = titles[job].text
            company = companies[job].text
            location = locations[job].text
            date = dates[job].text
            exp = experiences[job].text
            edu = educations[job].text
            url = "https://www.jobkorea.co.kr"+urls[job]['href']

            data.append({'Title': title, 'Company': company, 'Location': location, "Date": date, "experience" : exp, "education" : edu, "URL": url,})

        df = pd.DataFrame(data)
        try:
            writer = pd.ExcelWriter('jobs.xlsx', mode='a', engine='openpyxl', if_sheet_exists='overlay')

            max_row = writer.sheets[f'{dt_str}'].max_row

            if max_row == 1:
                df.to_excel(
                    writer,
                    sheet_name=f'{dt_str}',
                    startcol = 0,
                    startrow = 0,
                    index=False,
                    # encoding = 'utf-8',
                    na_rep = '',      # 결측값을 ''으로 채우기
                    inf_rep = '',     # 무한값을 ''으로 채우기
                    # header = None
                    )
                writer.close()
            else:
                df.to_excel(
                    writer, 
                    sheet_name=f'{dt_str}',
                    startcol = 0,
                    startrow = writer.sheets[f'{dt_str}'].max_row,
                    index=False,
                    # encoding = 'utf-8',
                    na_rep = '',      # 결측값을 ''으로 채우기
                    inf_rep = '',     # 무한값을 ''으로 채우기
                    header = None
                    )
                writer.close()              
        except:
            df.to_excel(
                excel_writer = 'jobs.xlsx',
                sheet_name = f'{dt_str}',
                index = False,       # 0부터 시작하는 자연수 인덱스는 의미가 없음.
                    # encoding = 'utf-8',
                na_rep = '',      # 결측값을 ''으로 채우기
                inf_rep = ''     # 무한값을 ''으로 채우기
            )     # 해당 파일이 열려있으면 안됨.    

        page_no += 1
        time.sleep(0.1)
    
# GET 요청을 처리하는 엔드포인트 정의
@app.get("/jobs", response_model=List[Job])
def get_jobs():
    if not os.path.exists('jobs.xlsx'):
        print('/jobs/ERROR: jobs.xlsx 파일이 존재하지 않습니다.')
        # 파일이 없을 경우 빈 데이터 반환 또는 오류 발생
        return []
    df = pd.read_excel('jobs.xlsx', engine="openpyxl")
    jobs = df.to_dict(orient='records')
    return jobs

def scrap_job():
    scrape_jobs_and_save_to_excel()

if __name__ == "__main__":
    scrap_job()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)