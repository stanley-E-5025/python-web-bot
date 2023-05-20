import sys, time, logging
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service


loger = logging.getLogger()


class ScraperClient:
    def __init__(self, url: str, steps: list):
        self.url = url
        self.steps = steps

    def extract_blob(self):
        chrome_options = Options()
        service = Service(executable_path="/path/to/chromedriver")
        
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": f"{root_dir}/downloads"},
        )
        window_size = self.steps["steps"][0]["width"], self.steps["steps"][0]["height"]

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        driver.set_window_size(window_size[0], window_size[1])

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
                        loger.info(f"Could not find element {selector}")

                if found_element:
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    actions = ActionChains(driver)
                    actions.move_to_element(element)

                    actions.click()
                    actions.perform()
                    time.sleep(15)

                else:
                    loger.info(f"Could not find element {selector}")

        driver.quit()
