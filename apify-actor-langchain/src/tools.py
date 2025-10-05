"""Module defines the tools used by the agent.

Feel free to modify or add new tools to suit your specific needs.

To learn how to create a new tool, see:
- https://python.langchain.com/docs/concepts/tools/
- https://python.langchain.com/docs/how_to/#tools
"""

from __future__ import annotations

import os
from apify import Actor
from apify_client import ApifyClient
from langchain_core.tools import tool

from src.models import InstagramPost, YCCompany, YCFounder, YCJob


def get_apify_client() -> ApifyClient:
    """Get or create ApifyClient with token from environment."""
    # Try to use Actor's client if available (when running in Apify platform)
    if hasattr(Actor, 'apify_client') and Actor.apify_client:
        return Actor.apify_client

    # Otherwise create a new client with token from environment
    token = os.getenv('APIFY_API_TOKEN')
    if not token:
        raise ValueError("APIFY_API_TOKEN not found in environment variables")

    return ApifyClient(token)


@tool
def tool_calculator_sum(numbers: list[int]) -> int:
    """Tool to calculate the sum of a list of numbers.

    Args:
        numbers (list[int]): List of numbers to sum.

    Returns:
        int: Sum of the numbers.
    """
    return sum(numbers)


@tool
async def tool_scrape_instagram_profile_posts(handle: str, max_posts: int = 30) -> list[InstagramPost]:
    """Tool to scrape Instagram profile posts.

    Args:
        handle (str): Instagram handle of the profile to scrape (without the '@' symbol).
        max_posts (int, optional): Maximum number of posts to scrape. Defaults to 30.

    Returns:
        list[InstagramPost]: List of Instagram posts scraped from the profile.

    Raises:
        RuntimeError: If the Actor fails to start.
    """
    run_input = {
        'directUrls': [f'https://www.instagram.com/{handle}/'],
        'resultsLimit': max_posts,
        'resultsType': 'posts',
        'searchLimit': 1,
    }
    if not (run := await Actor.apify_client.actor('apify/instagram-scraper').call(run_input=run_input)):
        msg = 'Failed to start the Actor apify/instagram-scraper'
        raise RuntimeError(msg)

    dataset_id = run['defaultDatasetId']
    dataset_items: list[dict] = (await Actor.apify_client.dataset(dataset_id).list_items()).items
    posts: list[InstagramPost] = []
    for item in dataset_items:
        url: str | None = item.get('url')
        caption: str | None = item.get('caption')
        alt: str | None = item.get('alt')
        likes: int | None = item.get('likesCount')
        comments: int | None = item.get('commentsCount')
        timestamp: str | None = item.get('timestamp')

        # only include posts with all required fields
        if not url or not likes or not comments or not timestamp:
            Actor.log.warning('Skipping post with missing fields: %s', item)
            continue

        posts.append(
            InstagramPost(
                url=url,
                likes=likes,
                comments=comments,
                timestamp=timestamp,
                caption=caption,
                alt=alt,
            )
        )

    return posts


# ============================================================================
# Y Combinator Scraper Tool
# ============================================================================

@tool
async def tool_scrape_yc_company(
    company_url: str,
    scrape_founders: bool = True,
    scrape_jobs: bool = True
) -> list[YCCompany]:
    """Scrape Y Combinator company data including founders and jobs.

    Args:
        company_url: URL of the YC company page or batch search (e.g.,
            "https://www.ycombinator.com/companies?batch=W25" or
            "https://www.ycombinator.com/companies/company-name")
        scrape_founders: Whether to scrape founder information
        scrape_jobs: Whether to scrape open job listings

    Returns:
        list[YCCompany]: List of YC companies with their profiles, founders, and jobs

    Raises:
        RuntimeError: If the Actor fails to start.
    """
    run_input = {
        'url': company_url,
        'scrape_founders': scrape_founders,
        'scrape_open_jobs': scrape_jobs,
        'scrape_all_companies': False
    }

    Actor.log.info(f'Starting Y Combinator scraper for: {company_url}')

    # Get Apify client
    client = get_apify_client()

    run = await client.actor('michael.g/y-combinator-scraper').call(
        run_input=run_input
    )

    if not run:
        msg = 'Failed to start the Actor michael.g/y-combinator-scraper'
        raise RuntimeError(msg)

    dataset_id = run['defaultDatasetId']
    dataset_items: list[dict] = (await client.dataset(dataset_id).list_items()).items

    companies: list[YCCompany] = []

    for item in dataset_items:
        # Extract basic company info
        company_name = item.get('company_name')
        company_id = item.get('company_id')

        if not company_name or not company_id:
            Actor.log.warning('Skipping company with missing name or ID: %s', item)
            continue

        # Parse founders
        founders_list: list[YCFounder] = []
        if scrape_founders and 'founders' in item and item['founders']:
            for founder_data in item['founders']:
                try:
                    founder = YCFounder(
                        id=founder_data.get('id', 0),
                        name=founder_data.get('name', ''),
                        linkedin=founder_data.get('linkedin')
                    )
                    founders_list.append(founder)
                except Exception as e:
                    Actor.log.warning(f'Failed to parse founder: {e}')
                    continue

        # Parse jobs
        jobs_list: list[YCJob] = []
        if scrape_jobs and 'open_jobs' in item and item['open_jobs']:
            for job_data in item['open_jobs']:
                try:
                    job = YCJob(
                        id=job_data.get('id', 0),
                        title=job_data.get('title', 'Unknown Position'),
                        description=job_data.get('description'),
                        location=job_data.get('location')
                    )
                    jobs_list.append(job)
                except Exception as e:
                    Actor.log.warning(f'Failed to parse job: {e}')
                    continue

        # Create company object
        try:
            company = YCCompany(
                company_id=company_id,
                company_name=company_name,
                batch=item.get('batch'),
                short_description=item.get('short_description'),
                long_description=item.get('long_description'),
                founders=founders_list,
                team_size=item.get('team_size'),
                tags=item.get('tags', []) if item.get('tags') else [],
                company_location=item.get('company_location'),
                website=item.get('website'),
                url=item.get('url'),
                open_jobs=jobs_list,
                is_hiring=item.get('is_hiring', False),
                company_linkedin=item.get('company_linkedin'),
                status=item.get('status'),
                year_founded=item.get('year_founded')
            )
            companies.append(company)
            Actor.log.info(f'Successfully parsed company: {company_name}')
        except Exception as e:
            Actor.log.error(f'Failed to create company object for {company_name}: {e}')
            continue

    Actor.log.info(f'Successfully scraped {len(companies)} companies')
    return companies
