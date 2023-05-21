import sys
import logging
import os
from pathlib import Path
from typing import List, Union
from pandas.core.frame import DataFrame

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from app.helpers.web_scraper import ScraperClient
from config import STEPS
import pandas as pd
import chardet


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ExecutePull:
    def __init__(self, scraper_client: ScraperClient):
        self.scraper_client = scraper_client

    @staticmethod
    def detect_encoding(file_path: str) -> str:
        with open(file_path, "rb") as rawdata:
            result = chardet.detect(rawdata.read(10000))
        return result["encoding"]

    @staticmethod
    def filter_unresolved_violations(file_path: str, encoding: str) -> DataFrame:
        data_frame = pd.read_csv(file_path, encoding=encoding, sep="\t")
        return data_frame[data_frame["Violation Resolved?"] == "No"]

    @staticmethod
    def overwrite_file(file_path: str, data_frame: DataFrame, new_file_name: str = None) -> None:
        os.remove(file_path)
        if new_file_name:
            directory = os.path.dirname(file_path)
            new_file_path = os.path.join(directory, new_file_name)
        else:
            new_file_path = file_path
        data_frame.to_csv(new_file_path, sep="\t", index=False)

    def execute(self) -> None:
        directory = self.scraper_client.extract_blob()
        reports = [elt for elt in os.listdir(directory) if elt.endswith(".csv")]
        property_violations = f"{directory}/{reports[0]}"

        encoding = self.detect_encoding(property_violations)
        unresolved_violations = self.filter_unresolved_violations(
            property_violations, encoding
        )

        self.overwrite_file(property_violations, unresolved_violations, "property_violations.csv")


if __name__ == "__main__":
    scraper_client = ScraperClient(
        url="https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
        steps=STEPS,
    )
    execute_pull = ExecutePull(
        scraper_client=scraper_client,
    )
    execute_pull.execute()  # Benchmark: 02:12.40
