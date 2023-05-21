import sys, logging, time, os, random
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
from datetime import datetime
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from faker import Faker


fake = Faker()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class ScraperClient:
    def __init__(self, url: str, steps: list, case:str, data:str):
        self.url = url
        self.steps = steps
        self.case = case
        self.data = data

    def handle_key_event(self, driver, key: str, action: str):
        if action == "keyDown":
            ActionChains(driver).key_down(getattr(Keys, key.upper())).perform()
        elif action == "keyUp":
            ActionChains(driver).key_up(getattr(Keys, key.upper())).perform()

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
                return element
            except:
                attempt += 1
                time.sleep(3)
                logger.info(
                    f"Attempt {attempt} to find element {selector} failed. Retrying..."
                )
        logger.info(f"Failed to find element {selector} after {retries} attempts.")
        return None

    def extract_blob(self) -> str:
        chrome_options = Options()
        executable_path = ""

        user_agents = [
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, {fake.name()} ) Chrome/113.0.0.0 Safari/537.36",
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, {fake.name()}) Chrome/58.0.3029.110 Safari/537.3",
            f"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, {fake.name()}) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, {fake.name()}) Chrome/41.0.2227.1 Safari/537.36",
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, {fake.name()}) Chrome/60.0.3112.113 Safari/537.36",
        ]

        user_agent = random.choice(user_agents)
        chrome_options.add_argument(f"user-agent={user_agent}")

        if platform.system() == "Windows":
            executable_path = f"{root_dir}/chromedriver_win32/chromedriver.exe"
        elif platform.system() == "Darwin":
            executable_path = f"{root_dir}chromedriver_mac64/chromedriver"
        else:
            executable_path = f"{root_dir}chromedriver_linux64/chromedriver"

        service = Service(executable_path=executable_path)

        today = datetime.today().strftime("%Y-%m-%d")
        download_dir = f"{root_dir}/downloads/{today}"
        os.makedirs(download_dir, exist_ok=True)
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": download_dir},
        )

        driver = webdriver.Chrome(service=service, options=chrome_options)
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        driver.get(self.url)
        driver.set_window_size(
            self.steps["steps"][0]["width"], self.steps["steps"][0]["height"]
        )

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
        )

        for step in self.steps["steps"]:
            if step["type"] == "click":
                for selector_group in step["selectors"]:
                    for selector in selector_group:
                        if (
                            "aria" not in selector
                            and "text" not in selector
                            and "xpath" not in selector
                        ):
                            by = By.CSS_SELECTOR
                            self.wait_for_element(driver, selector, by=by)
            elif step["type"] == "change":
                for selector_group in step["selectors"]:
                    for selector in selector_group:
                        if (
                            "aria" not in selector
                            and "text" not in selector
                            and "xpath" not in selector
                        ):

                            by = By.CSS_SELECTOR
                            element = self.wait_for_element(driver, selector, by=by)
                            if element:
                                element.clear()
                                element.send_keys(self.data)
                            
            elif step["type"] in ["keyDown", "keyUp"]:
                self.handle_key_event(driver, step["key"], step["type"])

        driver.quit()

        if self.case == "blob":
            return download_dir
        else:
            return None
