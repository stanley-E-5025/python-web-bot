import sys, logging, time
from pathlib import Path
import platform


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
import uuid

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class ScraperClient:
    def __init__(self, url: str, steps: list):
        self.url = url
        self.steps = steps

    def wait_for_element(self, driver, selector, by, retries=3):
        attempt = 0


        while attempt < retries:
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                actions = ActionChains(driver)
                actions.pause(1)
                actions.move_to_element(element)
                actions.click()
                actions.perform()
                return
            except:
                attempt += 1
                time.sleep(3)
                logger.info(
                    f"Attempt {attempt} to find element {selector} failed. Retrying..."
                )
        logger.info(f"Failed to find element {selector} after {retries} attempts.")

    def extract_blob(self):
        chrome_options = Options()
        executable_path = ""

        if platform.system() == "Windows":
            executable_path = f"{root_dir}/chromedriver_win32/chromedriver.exe"
        elif platform.system() == "Darwin":
            executable_path = f"{root_dir}chromedriver_mac64/chromedriver"
        else:
            executable_path = f"{root_dir}chromedriver_linux64/chromedriver"

        service = Service(executable_path=executable_path)
       
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": f"{root_dir}/downloads"},
        )
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        driver.set_window_size(
            self.steps["steps"][0]["width"], self.steps["steps"][0]["height"]
        )

        for step in self.steps["steps"]:
            if step["type"] == "click":
                for selector_group in step["selectors"]:
                    for selector in selector_group:
                        if "aria" not in selector and "text" not in selector and "xpath" not in selector:
                            by = By.CSS_SELECTOR
                            self.wait_for_element(driver, selector, by=by)

        driver.quit()
