import sys
import logging
import os
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from app.helpers.web_scraper import ScraperClient
from utils import detect_encoding, overwrite_file, filter


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ExecutePull:
    def __init__(self, scraper_client: ScraperClient):
        self.scraper_client = scraper_client

    def execute(self) -> str:
        directory = self.scraper_client.extract_blob()
        reports = [elt for elt in os.listdir(directory) if elt.endswith(".csv")]
        property_violations = f"{directory}/{reports[0]}"

        encoding = detect_encoding(property_violations)
        unresolved_violations = filter(
            file_path=property_violations,
            encoding=encoding,
            column="Violation Resolved?",
            expected="No",
        )

        new_file_path:str = overwrite_file(
            property_violations, unresolved_violations, "property_violations.csv"
        )

        return new_file_path
