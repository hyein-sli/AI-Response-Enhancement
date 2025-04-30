import os
import re
import time
import markdownify
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ───────────────────────────── 설정 ─────────────────────────────
MD_FOLDER = "./원천 데이터/web_md"
os.makedirs(MD_FOLDER, exist_ok=True)

URLS = [
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=10",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=100",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=101",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=102",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=103",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=104",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=105",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=106",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=107",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=108",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=109",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=11",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=110",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=111",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=112",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=113",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=114",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=115",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=116",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=117",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=118",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=119",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=12",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=120",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=121",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=122",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=123",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=124",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=125",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=126",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=127",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=128",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=129",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=13",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=130",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=131",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=132",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=133",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=134",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=135",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=136",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=137",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=138",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=139",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=14",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=140",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=141",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=142",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=143",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=144",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=145",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=146",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=147",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=148",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=149",
    "http://connect.kia.com/kr/04_customer/notice_view.html?idx=15",
    "http://connect.kia.com/kr/kiac_terms.html",
    "http://connect.kia.com/kr/kiap_terms.html",
    "http://connect.kia.com/kr/mozen_terms.html"
   
]


# ───────────────────────────── 유틸 ─────────────────────────────
def sanitize_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.lstrip("/").replace("/", ".")
    query = parsed.query.replace("=", "_").replace("&", "_")

    # 파일명 구성: path + query (있을 때만)
    if query:
        filename = f"{path}_{query}.md"
    else:
        filename = f"{path}.md"
    return filename

def strip_md_links(md: str) -> str:
    """본문 내 마크다운 링크/이미지 링크 제거(텍스트 유지)."""
    md = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", md)     # 이미지 링크
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)       # 일반 링크
    return md


def clean_markdown(md: str) -> str:
    """
    마크다운 정리:
      • 연속 개행을 단일 개행으로
      • '*' 문자 제거
      • 개행 직후 공백 제거
      • 각 줄의 선행 공백 제거  ← (NEW)
    """
    md = re.sub(r"\n{2,}", "\n", md)            # 연속 개행
    md = md.replace("*", "")
    md = re.sub(r"\n {2,}", "\n", md)           # 개행 뒤 공백
    md = re.sub(r"^[ \t]+", "", md, flags=re.MULTILINE)  # ← 선행 공백 제거
    return md


# ───────────────────────────── 크롤링 ─────────────────────────────
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
)

for base_url in URLS:
    try:
        print(f"\n▶ Processing: {base_url}")
        driver.get(base_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 헤더·푸터·네비게이션 제거
        for selector in ["header", "footer", "nav"]:
            for tag in soup.select(selector):
                tag.decompose()
        for tag in soup.find_all(True, id=re.compile("(?:^|_)header|footer", re.I)):
            tag.decompose()
        for tag in soup.find_all(True, class_=re.compile("(?:^|_)header|footer", re.I)):
            tag.decompose()

        # HTML → Markdown
        md_content = markdownify.markdownify(str(soup), heading_style="ATX")

        # 헤더 처리
        lines, first_header = [], False
        for line in md_content.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#"):
                if not first_header:
                    lines.append(f"# {base_url}")         # URL 유지
                    first_header = True
                else:
                    header_text = stripped.lstrip("#").strip()
                    lines.append(f"## {header_text}")     # H2 변환
            else:
                lines.append(line)

        md_content = "\n".join(lines)
        md_content = strip_md_links(md_content)   # 링크 제거
        md_content = clean_markdown(md_content)   # 최종 정리

        file_path = os.path.join(MD_FOLDER, sanitize_filename(base_url))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"✅ Saved → {file_path}")
    except Exception as e:
        print(f"❌ Error ({base_url}) → {e}")

driver.quit()
