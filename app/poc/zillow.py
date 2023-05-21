import sys
from pathlib import Path
import concurrent.futures

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from app.helpers.web_scraper import ScraperClient
from config import STEPS, STEPS2
from lambdas.pull_web_data import ExecutePull
from lambdas.search_web_data import ExecuteSearch
import pandas as pd
from utils import detect_encoding


report = []
bot_detected_values = []


def process_value(value):
    scraper_client = ScraperClient(
        url="https://www.zillow.com/", steps=STEPS2, case=None, data=value
    )
    execute_pull = ExecuteSearch(
        scraper_client=scraper_client,
    )

    result = execute_pull.execute()
    report.append(result)

    if result["bot_detected"]:
        bot_detected_values.append(value)


if __name__ == "__main__":
    scraper_client = ScraperClient(
        url="https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
        steps=STEPS,
        case="blob",
        data=None,
    )
    execute_pull = ExecutePull(
        scraper_client=scraper_client,
    )

    address = execute_pull.execute()

    encoding = detect_encoding(address)
    data_frame = pd.read_csv(address, encoding=encoding, sep="\t")
    column = data_frame["Address"].to_list()
    column = column[:10]

    while column:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_value, column)

        column = bot_detected_values.copy()
        bot_detected_values.clear()

    print(report)
