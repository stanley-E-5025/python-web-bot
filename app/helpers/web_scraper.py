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
from utils import generate_user_agent


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class ScraperClient:
    def __init__(self, url: str, steps: list, case: str, data: str):
        self.url = url
        self.steps = steps
        self.case = case
        self.data = data
        self.bot_detected = False

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

    def extract_blob(self) -> dict:
        chrome_options = Options()
        executable_path = ""
        user_agent = generate_user_agent()
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

        current_url = driver.current_url

        while "captchaPerimeter" in current_url:
            self.bot_detected = True
            for selector_group in [
                ["#px-captcha"],
            ]:
                for selector in selector_group:
                    if "aria" in selector or "text" in selector or "xpath" in selector:
                        by = By.XPATH
                    else:
                        by = By.CSS_SELECTOR

                    element = self.wait_for_element(driver, selector, by=by)
                    if element:
                        break
                if element:
                    break

            # Hold a click on the captcha element
            if element:
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(element, 137, 24)
                actions.click_and_hold().perform()

                # Wait until the URL changes
                WebDriverWait(driver, 60).until(EC.url_changes(current_url))
                time.sleep(3)

                actions.release().perform()

            current_url = driver.current_url

        if "captchaPerimeter" in current_url:
            return {
                "bot_detected": self.bot_detected,
                "case": self.case,
                "data": self.data,
                "url": self.url,
                "blob": None,
            }

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

        return {
            "bot_detected": self.bot_detected,
            "download_dir": download_dir,
            "data": self.data,
            "case": self.case,
        }
