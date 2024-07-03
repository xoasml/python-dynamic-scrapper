from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup


p = sync_playwright().start()

# .launch(headless=True) 가 디폴트이며 True일때 백그라운드에서 작업 된다.
# False 일 때는 실제로 브라우저가 작동 하는걸 볼수 있다.
browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/")

time.sleep(2)

page.click("button.Aside_searchButton__rajGo")

time.sleep(2)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

time.sleep(2)

page.keyboard.down("Enter")

time.sleep(4)

page.click("a#search_tab_position")

time.sleep(2)

for x in range(5):
    page.keyboard.down("End")
    time.sleep(1)


time.sleep(3)

content = page.content()

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__REty8")

job_datas=[]

for job in jobs:
    url = job.find("a")["href"]
    title = job.find("strong", class_="JobCard_title__HBpZf")
    company = job.find("span", class_="JobCard_companyName__N1YrF")

    data = {
        "url" : f"https://www.wanted.co.kr{url}",
        "title" : title.text,
        "company" : company.text,

    }

    job_datas.append(data)

print(job_datas)