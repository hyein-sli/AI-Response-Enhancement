import os
import fitz  # PyMuPDF

# 1. 루트 경로 설정
base_dir = r"C:\Users\leehyein\Documents\code\kia\AI-Response-Enhancement\선광 아카이브"
output_md_dir = os.path.join(base_dir, "원천데이터")

# 2. 출력 폴더 없으면 생성
os.makedirs(output_md_dir, exist_ok=True)

# 3. PDF → MD 변환 함수
def convert_pdf_to_md(pdf_path, md_path, title_prefix):
    doc = fitz.open(pdf_path)
    pdf_name = os.path.basename(pdf_path)

    with open(md_path, 'w', encoding='utf-8') as md_file:
        md_file.write(f"# {title_prefix} {pdf_name} 추출 결과\n\n")
        for i, page in enumerate(doc, start=1):
            text = page.get_text()
            if text.strip():
                md_file.write(f"## 페이지 {i}\n\n{text}\n\n")
    doc.close()

# 4. 연도별 폴더 순회하며 PDF 처리
for year in os.listdir(base_dir):
    year_path = os.path.join(base_dir, year)
    
    if os.path.isdir(year_path) and year.isdigit():
        year_int = int(year)

        # 2019년 이상은 '국문' 폴더 안만 처리
        if year_int >= 2019:
            korean_path = os.path.join(year_path, "국문")
            if os.path.exists(korean_path):
                target_path = korean_path
            else:
                continue  # 국문 폴더 없으면 스킵
        else:
            target_path = year_path

        # 해당 폴더 내 모든 PDF 파일 처리
        for filename in os.listdir(target_path):
            if filename.lower().endswith(".pdf"):
                pdf_file_path = os.path.join(target_path, filename)
                md_file_name = f"{year}_{os.path.splitext(filename)[0]}.md"
                md_file_path = os.path.join(output_md_dir, md_file_name)

                convert_pdf_to_md(pdf_file_path, md_file_path, year)

print("✅ 모든 PDF → MD 변환 완료! '원천데이터' 폴더를 확인해주세요.")
