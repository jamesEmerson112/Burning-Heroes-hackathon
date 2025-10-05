"""Standalone test for Y Combinator scraper - Direct ApifyClient usage."""

import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient


def initialize_client() -> ApifyClient:
    """Initialize and return ApifyClient with API token."""
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)

    api_token = os.getenv('APIFY_API_TOKEN')
    if not api_token:
        raise ValueError("APIFY_API_TOKEN not found in .env file")

    return ApifyClient(api_token)


def run_scraper(client: ApifyClient, url: str) -> dict:
    """Run the YC scraper and return run metadata."""
    run_input = {
        "scrape_founders": True,
        "scrape_open_jobs": True,
        "url": url,
        "scrape_all_companies": False,
    }

    print(f"🚀 Starting YC Scraper")
    print(f"📍 URL: {url}")
    print(f"⏳ Running actor...", end=" ", flush=True)

    run = client.actor("michael.g/y-combinator-scraper").call(run_input=run_input)

    print("✓")
    return run


def save_json_results(companies: list, output_dir: Path, timestamp: str) -> Path:
    """Save companies data to JSON file."""
    json_file = output_dir / f'yc_scraper_results_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    return json_file


def save_text_report(companies: list, output_dir: Path, timestamp: str, dataset_id: str) -> Path:
    """Save formatted text report."""
    txt_file = output_dir / f'yc_scraper_report_{timestamp}.txt'

    with open(txt_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("="*80 + "\n")
        f.write("Y COMBINATOR SCRAPER RESULTS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Companies: {len(companies)}\n")
        f.write(f"Dataset URL: https://console.apify.com/storage/datasets/{dataset_id}\n")
        f.write("\n" + "="*80 + "\n\n")

        # Company details
        for i, company in enumerate(companies, 1):
            f.write(f"\n{'─'*80}\n")
            f.write(f"Company #{i}: {company.get('company_name', 'Unknown')}\n")
            f.write(f"{'─'*80}\n\n")

            # Basic info
            f.write("BASIC INFORMATION:\n")
            f.write(f"  • ID: {company.get('company_id')}\n")
            f.write(f"  • Batch: {company.get('batch', 'N/A')}\n")
            f.write(f"  • Team Size: {company.get('team_size', 'N/A')}\n")
            f.write(f"  • Year Founded: {company.get('year_founded', 'N/A')}\n")
            f.write(f"  • Status: {company.get('status', 'N/A')}\n")
            f.write(f"  • Location: {company.get('company_location', 'N/A')}\n")
            f.write(f"  • Website: {company.get('website', 'N/A')}\n")
            f.write(f"  • YC URL: {company.get('url', 'N/A')}\n")
            f.write(f"  • LinkedIn: {company.get('company_linkedin', 'N/A')}\n")
            f.write(f"  • Is Hiring: {company.get('is_hiring', False)}\n\n")

            # Description
            if company.get('short_description'):
                f.write("SHORT DESCRIPTION:\n")
                f.write(f"  {company['short_description']}\n\n")

            if company.get('long_description'):
                f.write("LONG DESCRIPTION:\n")
                f.write(f"  {company['long_description']}\n\n")

            # Tags
            if company.get('tags'):
                f.write("TAGS:\n")
                f.write(f"  {', '.join(company['tags'])}\n\n")

            # Founders
            if company.get('founders'):
                f.write(f"FOUNDERS ({len(company['founders'])}):\n")
                for founder in company['founders']:
                    name = founder.get('name', 'N/A')
                    linkedin = founder.get('linkedin', 'N/A')
                    f.write(f"  • {name}\n")
                    if linkedin != 'N/A':
                        f.write(f"    LinkedIn: {linkedin}\n")
                f.write("\n")

            # Jobs
            if company.get('open_jobs'):
                f.write(f"OPEN POSITIONS ({len(company['open_jobs'])}):\n")
                for job in company['open_jobs']:
                    title = job.get('title', 'N/A')
                    location = job.get('location', 'N/A')
                    f.write(f"  • {title} @ {location}\n")
                    if job.get('description'):
                        desc = job['description'][:100] + "..." if len(job['description']) > 100 else job['description']
                        f.write(f"    {desc}\n")
                f.write("\n")

        # Data structure reference
        f.write("\n" + "="*80 + "\n")
        f.write("DATA STRUCTURE REFERENCE (First Company)\n")
        f.write("="*80 + "\n\n")
        first_company = companies[0]
        f.write("Available fields:\n")
        for key in sorted(first_company.keys()):
            value_type = type(first_company[key]).__name__
            f.write(f"  • {key}: {value_type}\n")

    return txt_file


def main():
    """Main execution."""
    try:
        # Initialize
        client = initialize_client()

        # Run scraper
        url = "https://www.ycombinator.com/companies"
        run = run_scraper(client, url)

        # Get results
        dataset_id = run['defaultDatasetId']
        companies = list(client.dataset(dataset_id).iterate_items())

        if not companies:
            print("⚠️  No companies found")
            return

        print(f"✅ Scraped {len(companies)} companies")

        # Save results
        output_dir = Path(__file__).parent / 'test_results'
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        json_file = save_json_results(companies, output_dir, timestamp)
        txt_file = save_text_report(companies, output_dir, timestamp, dataset_id)

        # Summary
        print(f"💾 JSON: {json_file.name}")
        print(f"📄 Report: {txt_file.name}")
        print(f"📁 Location: {output_dir}")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()
