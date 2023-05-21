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

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ExecuteSearch:
    def __init__(self, scraper_client: ScraperClient):
        self.scraper_client = scraper_client
    def execute(self) -> dict:
        data = self.scraper_client.extract_blob()
        return data

