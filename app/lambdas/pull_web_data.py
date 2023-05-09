import sys, time, os
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app.helpers.web_scraper import ScraperClient
from app.helpers.email_client import EmailClient
from app.api_clients.openai_client import OpenAIClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from config import STEPS


class ExecutePull:
    def __init__(
        self,
        scraper_client: ScraperClient,
        email_client: EmailClient,
        openai_client: OpenAIClient,
        steps: dict,
        url: str,
    ):
        self.scraper_client = scraper_client
        self.email_client = email_client
        self.openai_client = openai_client
        self.steps = steps
        self.url = url
        self.window_size = steps["steps"][0]["width"], steps["steps"][0]["height"]

    def execute(self):
        chrome_options = Options()
        service = Service(executable_path="/path/to/chromedriver")
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": "/Users/koloni/Desktop/koloni_tools/app"},
        )

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        driver.set_window_size(self.window_size[0], self.window_size[1])

        time.sleep(10)

        for step in self.steps["steps"]:
            if step["type"] == "click":
                selectors = step["selectors"]
                found_element = False
                for selector_group in selectors:
                    try:
                        for selector in selector_group:
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.CSS_SELECTOR, selector)
                                )
                            )

                            found_element = True
                            break
                    except:
                        pass

                if found_element:
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    actions = ActionChains(driver)
                    actions.move_to_element(element)

                    actions.click()
                    actions.perform()
                    time.sleep(12)

                else:
                    print(step)

        driver.quit()


if __name__ == "__main__":
    scraper_client = ScraperClient()
    email_client = EmailClient(email="stanleygordon45@gmail.com", password="222004stan")
    openai_client = OpenAIClient()

    execute_pull = ExecutePull(
        scraper_client=scraper_client,
        email_client=email_client,
        openai_client=openai_client,
        steps=STEPS,
        url="https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
    )
    execute_pull.execute()
