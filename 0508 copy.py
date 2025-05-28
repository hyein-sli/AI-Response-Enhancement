import os
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ───────────── 설정 ─────────────
MD_FOLDER = "./원천 데이터/web_md/0528"
os.makedirs(MD_FOLDER, exist_ok=True)

URLS = [
   "https://members.kia.com/kr/view/qmgd/qmgd_partnershipCard01.do",
"https://members.kia.com/kr/view/qmgd/qmgd_partnershipCard01_ev.do",
"https://members.kia.com/kr/view/qmgd/qmgd_qmembers_ev.do",
"https://members.kia.com/kr/view/qmgd/qmgd_qmemberscom.do",
"https://members.kia.com/kr/view/qmgt/bt_itca/qmgt_bt_itca_bluetooth.do",
"https://members.kia.com/kr/view/qmgt/navi/qmgt_navi_guide.do",
"https://members.kia.com/kr/view/qmnb/mbr_card/qmnb_mbr_card_reissue.do",
"https://members.kia.com/kr/view/qnet/asn_prct/qnet_asn_prct_index.do",
"https://members.kia.com/kr/view/qnet/dtd_svc/qnet_dtd_svc_smartQsvcList02.do",
"https://members.kia.com/kr/view/qnet/info/qnet_solution.do"

]

def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    fragment = parsed.fragment.replace("#", "_")
    query = parsed.query.replace("=", "_").replace("&", "_")

    filename = path
    if fragment:
        filename += f"_{fragment}"
    if query:
        filename += f"_{query}"
    return f"{filename}.md"

# ───────────── 셀레니움 설정 ─────────────
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ───────────── 크롤링 반복 ─────────────
for url in URLS:
    try:
        driver.get(url)
        time.sleep(3)  # JS 렌더링 대기

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 불필요 요소 제거
        for tag in soup.select("header, footer, nav, script, style"):
            tag.decompose()

        # 텍스트 추출
        main_text = soup.get_text(separator="\n", strip=True)

        # 파일명 및 저장
        filename = sanitize_filename(url)
        filepath = os.path.join(MD_FOLDER, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {url}\n\n")
            f.write(main_text)

        print(f"✅ 저장 완료: {filepath}")
    
    except Exception as e:
        print(f"❌ 오류 발생 ({url}) → {e}")

driver.quit()
