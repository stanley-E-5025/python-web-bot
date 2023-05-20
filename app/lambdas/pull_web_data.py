import sys, logging
from pathlib import Path

tenant_directory, root_dir = (
    Path(__file__).resolve().parent.parent,
    Path(__file__).resolve().parent.parent.parent,
)
sys.path.insert(0, str(root_dir))
sys.path.append(str(tenant_directory))

from app.helpers.web_scraper import ScraperClient
from config import STEPS

logger = logging.getLogger()
logger.setLevel(logging.INFO)
class ExecutePull:
    def __init__(
        self,
        scraper_client: ScraperClient,
    ):
        self.scraper_client = scraper_client

    def execute(self):
        logger.info("Starting pull")
        self.scraper_client.extract_blob()
        logger.info("Finished pull")

       
if __name__ == "__main__":
    scraper_client = ScraperClient(
        url="https://tableau.minneapolismn.gov/views/OpenDataRegulatoryServices-Violations/PropertySearch?%3Aiid=2&%3AisGuestRedirectFromVizportal=y&%3Aembed=y",
        steps=STEPS,
    )
    execute_pull = ExecutePull(
        scraper_client=scraper_client,
    )
    execute_pull.execute() # Bentchmark: 02:12.40
    
