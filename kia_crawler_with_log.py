
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
from datetime import datetime
import json
import time

# 엑셀 파일 경로
excel_path = r"C:\Users\leehyein\Documents\code\kia\AI-Response-Enhancement\worldwide_kia.xlsx"

# JSON 출력 파일 경로
output_path = "kia_crawled_data2.json"

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 크롬 드라이버 서비스 초기화
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# 날짜
today_str = datetime.today().strftime("%Y-%m-%d")

# 엑셀에서 URL 읽기
wb = load_workbook(excel_path)
ws = wb.active
urls = [cell.value for cell in ws['A'] if cell.value and str(cell.value).startswith('http')]

data = []
success_urls = []
failed_urls = []

for url in urls:
    try:
        print(f"🟡 크롤링 시도 중: {url}")
        driver.get(url)
        time.sleep(2)
        body_text = driver.find_element(By.TAG_NAME, "body").text.strip()

        entry = {
            "url": url,
            "rawDataFormat": "web",
            "rawDataExtractionDate": today_str,
            "text": body_text,
            "category": [],
            "query": []
        }

        data.append(entry)
        success_urls.append(url)
        print(f"✅ 성공: {url}")

    except Exception as e:
        failed_urls.append(url)
        print(f"❌ 실패: {url} | 이유: {e}")

driver.quit()

# JSON 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 결과 요약 출력
print("\n=======================")
print(f"✅ 크롤링 성공 주소 수: {len(success_urls)}")
for s in success_urls:
    print(f" - {s}")

print(f"❌ 크롤링 실패 주소 수: {len(failed_urls)}")
for f in failed_urls:
    print(f" - {f}")
print("=======================")
