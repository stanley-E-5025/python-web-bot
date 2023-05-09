import sys
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScraperClient:
    def __init__(self):
        self.session = requests.Session()
        self.driver = webdriver.Chrome(executable_path="path/to/chromedriver")

    def fetch_page_content(self, url):
        chrome_options = Options()
        chrome_options.headless = True

        driver = webdriver.Chrome(
            executable_path="/path/to/chromedriver", options=chrome_options
        )

        driver.get(url)
        page_content = driver.page_source

        driver.quit()

        return page_content

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        return soup

    def extract_data(self, soup, css_selector):
        elements = soup.select(css_selector)
        return elements

    def download_file(self, url, file_name):
        response = self.session.get(url)
        with open(file_name, "wb") as f:
            f.write(response.content)

    def interact_with_page(
        self, url, element_css_selector, interaction_type, input_value=None
    ):
        self.driver.get(url)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_css_selector))
        )

        if interaction_type == "click":
            element.click()
        elif interaction_type == "input":
            element.send_keys(input_value)
        elif interaction_type == "select":
            select = webdriver.support.ui.Select(element)
            select.select_by_visible_text(input_value)

    def quit_driver(self):
        self.driver.quit()
