import os
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 설정
MD_FOLDER = "./원천 데이터/web_md"
os.makedirs(MD_FOLDER, exist_ok=True)
url = "https://www.kia.com/kr/vehicles/kia-ev/guide/faq#localnav"

# 파일명 생성
def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    return f"{path}.md"

# 셀레니움 설정
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")

# FAQ 영역 텍스트 수집
content_parts = []
faq_blocks = soup.select("div.accordion-item, div.tab-content, div.faq-content, dl.faq")

for block in faq_blocks:
    text = block.get_text(separator="\n", strip=True)
    if text:
        content_parts.append(text)

final_text = "\n\n".join(content_parts)

# 마크다운 저장
filename = sanitize_filename(url)
filepath = os.path.join(MD_FOLDER, filename)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"# {url}\n\n{final_text.strip()}")

driver.quit()
print(f"✅ 저장 완료: {filepath}")
