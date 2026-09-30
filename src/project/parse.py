from playwright.sync_api import sync_playwright


def getRawHtml(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()

        response = page.goto(url)

        status_code = response.status if response else None

        if status_code != 200:
            browser.close()
            raise Exception(f"HTTP_ERROR:{status_code}")
        
        page.wait_for_timeout(20000)

        html = page.content()
        

        browser.close()

        return html