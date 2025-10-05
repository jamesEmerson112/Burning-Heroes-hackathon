"""Test script for Y Combinator scraper tool."""

import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from apify import Actor
from src.tools import tool_scrape_yc_company

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_yc_scraper():
    """Test the YC scraper with a W25 batch query."""
    logger.info("Starting YC scraper test...")

    async with Actor:
        # Test with a specific YC batch
        test_url = "https://www.ycombinator.com/companies?batch=W25"

        logger.info(f"Testing with URL: {test_url}")

        try:
            # Call the scraper tool
            companies = await tool_scrape_yc_company.ainvoke({
                "company_url": test_url,
                "scrape_founders": True,
                "scrape_jobs": True
            })

            logger.info(f"\n{'='*60}")
            logger.info(f"✅ Successfully scraped {len(companies)} companies")
            logger.info(f"{'='*60}\n")

            # Display first 3 companies as sample
            for i, company in enumerate(companies[:3], 1):
                logger.info(f"\n--- Company {i}: {company.company_name} ---")
                logger.info(f"Batch: {company.batch}")
                logger.info(f"One-liner: {company.one_liner}")
                logger.info(f"Industries: {', '.join(company.industries)}")
                logger.info(f"Team Size: {company.team_size}")
                logger.info(f"Website: {company.website}")
                logger.info(f"Founders: {len(company.founders)}")
                logger.info(f"Open Jobs: {len(company.jobs)}")

                if company.founders:
                    logger.info("\nFounders:")
                    for founder in company.founders[:2]:  # Show first 2 founders
                        logger.info(f"  - {founder.first_name} {founder.last_name} ({founder.title})")

                if company.jobs:
                    logger.info("\nOpen Positions:")
                    for job in company.jobs[:2]:  # Show first 2 jobs
                        logger.info(f"  - {job.title} @ {job.location}")

            logger.info(f"\n{'='*60}")
            logger.info("✅ TEST PASSED: YC Scraper is working correctly!")
            logger.info(f"{'='*60}\n")

            return companies

        except Exception as e:
            logger.error(f"❌ TEST FAILED: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(test_yc_scraper())
