from playwright.sync_api import sync_playwright


class Browser:

    def __enter__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True
        )

        self.page = self.browser.new_page(
            viewport={
                "width": 1600,
                "height": 900
            }
        )

        return self.page

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.browser.close()

        self.playwright.stop()