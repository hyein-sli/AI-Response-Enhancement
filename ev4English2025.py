# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# try:
#     # 크롬 드라이버 실행
#     driver = webdriver.Chrome()

#     # 웹페이지 열기
#     driver.get("https://ownersmanual.kia.com/manual/EV6?langCode=en_US&countryCode=B28&projCode=CV1&year=2024")

#     # iframe 안으로 진입 (iframe이 1개니까 index 0 사용)
#     WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

#     # Electric vehicle guide 클릭
#     ev_guide_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-id='t00002']"))
#     )
#     ev_guide_link.click()
#     print("클릭 성공!")

#     # 확인을 위해 잠깐 대기
#     time.sleep(5)

# except Exception as e:
#     print("에러 발생:", e)

# finally:
# # 꺼지지 않도록 일단 주석처리
# # driver.quit()
#   pass
# # 이후 작업 진행...

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://ownersmanual.kia.com/manual/EV6?langCode=en_US&countryCode=B28&projCode=CV1&year=2024")

try:
    # iframe 전환
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # Electric vehicle guide 클릭
    ev_guide_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-id='t00002']"))
    )
    ev_guide_link.click()
    print("EV Guide 클릭 성공")
    time.sleep(1)  # 페이지 전환 대기

    # Overview of electric vehicle 클릭
    overview_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a#t00003-d7794e48-link"))
    )
    overview_link.click()
    print("Overview 클릭 성공")
    time.sleep(3)

except Exception as e:
    print("에러 발생:", e)

finally:
    pass  # 테스트 끝난 뒤에 driver.quit()으로 종료

