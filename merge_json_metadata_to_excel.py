import json
import pandas as pd

# 파일 경로 설정
json_path = r"C:\Users\leehyein\Desktop\기아 프로젝트\납품\도메인분류_데이터_컨텐츠_20250618_v0.2.json"
excel_path = r"C:\Users\leehyein\Desktop\metadata.xlsx"

# JSON 파일 로드
with open(json_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 메타데이터 리스트 생성
metadata_list = []
for idx, item in enumerate(json_data):
    metadata = {
        "index": idx,
        "rawDataFormat": item.get("rawDataFormat"),
        "rawDataExtractionDate": item.get("rawDataExtractionDate"),
        "source": item.get("source"),
        "url": item.get("url"),
        "category": item.get("category"),
        "query": ", ".join(item.get("query", [])),  # 리스트를 문자열로 변환
    }
    metadata_list.append(metadata)

# DataFrame 변환
metadata_df = pd.DataFrame(metadata_list)

# 기존 엑셀 불러오기
existing_excel = pd.read_excel(excel_path)

# 기존 데이터와 메타데이터 병합
merged_df = pd.concat([existing_excel, metadata_df], axis=1)

# 결과 저장
output_path = "metadata_with_chunks.xlsx"
merged_df.to_excel(output_path, index=False)
