from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

URL = "https://cafe.naver.com/f-e/cafes/24845809/menus/0"
OUT = "naver_cafe.csv"
MAX_PAGES = 45  # 원하는 만큼

def scrape_current_page(html: str, page_no: int):
    soup = BeautifulSoup(html, "html.parser")

    authors = [x.get_text(strip=True) for x in soup.select("span.nickname")]
    dates   = [x.get_text(strip=True) for x in soup.select("td.td_normal.type_date")]

    m = min(len(authors), len(dates))
    rows = []
    for i in range(m):
        rows.append({
            "page": page_no,
            "author": authors[i],
            "datetime": dates[i],
        })
    return rows, len(authors), len(dates), m

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    number_btns = page.locator("button.btn.number")
    next_btn = page.locator('button.btn.type_next[aria-label="다음"]')

    # 페이지 번호 버튼 뜰 때까지
    number_btns.first.wait_for(timeout=15000)

    all_rows = []

    # 1~MAX_PAGES를 10개씩 끊어서 처리
    for group_start in range(1, MAX_PAGES + 1, 10):
        group_end = min(group_start + 9, MAX_PAGES)

        # 11~20, 21~30... 로 넘어갈 때마다 "다음" 1회 클릭
        if group_start != 1:
            next_btn.click()
            # 새 그룹의 첫 페이지 번호가 나타날 때까지 대기 (예: 11, 21, 31 ...)
            page.locator("button.btn.number").filter(has_text=str(group_start)).first.wait_for(timeout=15000)

        # 해당 그룹(예: 11~20) 안에서 페이지 하나씩 클릭/스크랩
        for page_no in range(group_start, group_end + 1):
            page.locator("button.btn.number").filter(has_text=str(page_no)).first.click()

            # 클릭 후 컨텐츠 로딩 대기 (임시)
            time.sleep(1.2)

            rows, a_cnt, d_cnt, saved = scrape_current_page(page.content(), page_no)
            all_rows.extend(rows)

            print(f"[{page_no}] authors={a_cnt}, dates={d_cnt}, saved={saved}")

    browser.close()

# CSV 저장
with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["page", "author", "datetime"])
    w.writeheader()
    w.writerows(all_rows)

print("완료:", OUT)