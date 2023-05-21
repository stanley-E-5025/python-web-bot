import sys
import logging
from pathlib import Path


tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from app.helpers.web_scraper import ScraperClient
from config import STEPS2

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ExecutePull:
    def __init__(self, scraper_client: ScraperClient):
        self.scraper_client = scraper_client
    def execute(self) -> None:
        self.scraper_client.extract_blob()

if __name__ == "__main__":
    scraper_client = ScraperClient(
        url="https://www.zillow.com/",
        steps=STEPS2,
    )
    execute_pull = ExecutePull(
        scraper_client=scraper_client,
    )
    execute_pull.execute() 
