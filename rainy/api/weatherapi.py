import requests
from dotenv import load_dotenv
import os 

# load .env
load_dotenv()

api_key = os.environ.get('api')
print(api_key)

# url = 'https://www.naver.com/'
url = f'https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?authKey={api_key}&numOfRows=10&pageNo=1&base_date=20210628&base_time=0600&nx=55&ny=127'
response = requests.get(url)
print(response.status_code)
print(response.content)