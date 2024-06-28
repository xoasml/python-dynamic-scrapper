from playwright.sync_api import sync_playwright

p = sync_playwright().start()

# .launch(headless=True) 가 디폴트이며 True일때 백그라운드에서 작업 된다.
# False 일 때는 실제로 브라우저가 작동 하는걸 볼수 있다.
browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://google.com")

page.screenshot(path="screenshot.png")