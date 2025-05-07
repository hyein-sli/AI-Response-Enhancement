import os
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ───────────── 설정 ─────────────
MD_FOLDER = "./원천 데이터/web_md"
os.makedirs(MD_FOLDER, exist_ok=True)
url = "https://www.kia.com/kr/vehicles/kia-ev/vehicles#localnav"

def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_").replace("#", "")
    return f"{path}.md"

# ───────────── 셀레니움 설정 ─────────────
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ───────────── 페이지 로딩 및 대기 ─────────────
driver.get(url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "vehicle-card"))
    )
except:
    print("❌ 차량 카드 로딩 실패")
    driver.quit()
    exit()

# ───────────── BeautifulSoup 파싱 ─────────────
soup = BeautifulSoup(driver.page_source, "html.parser")

# ───────────── 차량 정보 추출 ─────────────
content_parts = []
cards = soup.select("div.vehicle-card")

for card in cards:
    title_tag = card.select_one("strong")
    desc_tag = card.select_one("p")

    title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
    desc = desc_tag.get_text(strip=True) if desc_tag else ""

    content_parts.append(f"## {title}\n\n{desc}")

# ───────────── 마크다운 저장 ─────────────
filename = sanitize_filename(url)
filepath = os.path.join(MD_FOLDER, filename)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(f"# {url}\n\n")
    f.write("\n\n".join(content_parts))

driver.quit()
print(f"✅ 저장 완료: {filepath}")
