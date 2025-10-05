# YC Scraper Test Analysis

**Date:** October 4, 2025
**Test Run:** test_yc_standalone.py
**Companies Scraped:** 25 (free tier limit)

## Summary

Successfully scraped Y Combinator company data using the Apify actor `michael.g/y-combinator-scraper`. Generated both JSON and text report outputs for analysis.

## Key Findings

### 1. Data Structure

The actual API response contains these fields:

```
• batch: str (e.g., "Summer 2025", "Winter 2014")
• company_id: int
• company_image: str (logo URL)
• company_linkedin: str
• company_location: str
• company_name: str
• company_x: str (Twitter/X handle)
• founders: list (contains dict with id, name, linkedin)
• is_hiring: bool
• long_description: str
• number_of_open_jobs: int
• open_jobs: list (can be None or list of dicts)
• primary_partner: str (YC partner name)
• short_description: str
• status: str (e.g., "ACTIVE")
• tags: list (industry tags)
• team_size: str (can be int or string)
• url: str (YC profile URL)
• website: str
• year_founded: str (can be int or null)
```

### 2. Field Mapping (Current Models vs Actual Data)

#### ✅ Correctly Mapped:
- `company_id` → `company_id`
- `company_name` → `company_name`
- `batch` → `batch`
- `website` → `website`
- `status` → `status`
- `is_hiring` → `is_hiring`
- `founders` → `founders` (with adjustments)
- `open_jobs` → `open_jobs` (with adjustments)

#### ⚠️ Needs Adjustment:
- `company_location` (API) vs `company_location` (model) ✓ Matches
- `company_linkedin` (API) vs `company_linkedin` (model) ✓ Matches
- `short_description` (API) vs `short_description` (model) ✓ Matches
- `long_description` (API) vs `long_description` (model) ✓ Matches
- `tags` (API) vs `tags` (model) ✓ Matches
- `team_size` (API) - mixed type (str/int)
- `year_founded` (API) - mixed type (str/int/None)

#### 🆕 Additional Fields in API (not in our model):
- `company_image` - Logo URL
- `company_x` - Twitter/X handle
- `primary_partner` - YC partner name
- `number_of_open_jobs` - Count of open positions

#### ❌ Fields in Model Not in API:
- `url` is present (YC profile URL) ✓

### 3. Founder Data Structure

**API Structure:**
```json
{
  "id": 1919921,
  "name": "Pranav Madhukar",
  "linkedin": "https://www.linkedin.com/in/pranav-madhukar-pcm/"
}
```

**Our Model:** ✅ Matches correctly
```python
class YCFounder(BaseModel):
    id: int
    name: str
    linkedin: str | None = None
```

### 4. Job Data Structure

**API Structure:**
```json
{
  "id": 81974,
  "title": "Founding Engineer",
  "description": "...",
  "location": "San Francisco, CA, US"
}
```

**Our Model:** ✅ Matches correctly
```python
class YCJob(BaseModel):
    id: int
    title: str
    description: str | None = None
    location: str | None = None
```

## Data Quality Observations

### Good Quality:
- ✅ Company names consistently present
- ✅ Founder data well-structured when available
- ✅ Batch information accurate
- ✅ Website URLs properly formatted
- ✅ Job listings have good detail when present

### Inconsistencies:
- ⚠️ `team_size` - Sometimes string, sometimes int ("2" vs 2)
- ⚠️ `year_founded` - Can be string, int, or None
- ⚠️ `open_jobs` - Can be None or empty list when no jobs
- ⚠️ `tags` - Can be None or list
- ⚠️ Some founder records missing LinkedIn URLs

## Recommendations

### 1. Model Updates Needed ✅ (Already Done)
Our current models are accurate and match the API structure.

### 2. Add Optional Fields
Consider adding these useful fields to YCCompany model:
```python
company_image: str | None = None  # Logo
company_x: str | None = None  # Twitter handle
primary_partner: str | None = None  # YC partner
number_of_open_jobs: int = 0
```

### 3. Type Handling
Handle mixed types gracefully:
- `team_size`: Accept both `int` and `str`
- `year_founded`: Accept `int`, `str`, or `None`
- `tags`: Handle both `None` and empty lists

### 4. Tool Implementation ✅ (Already Done)
Our tool in `src/tools.py` correctly parses the API response.

## Sample Companies Analyzed

1. **Meteor** (S25) - AI-Native Browser, 2 team members
2. **Algolia** (W14) - Search API, 810 team members (acquired/large)
3. **Perspectives Health** (S25) - Healthcare IT with 3 open positions
4. **Humoniq** (S25) - AI BPO for travel, actively hiring
5. **Kontigo** (S24) - Fintech neobank, 10 team members

## Next Steps

1. ✅ Models validated against real data
2. ✅ Tool implementation verified
3. ⏳ Test integration with LangChain agent
4. ⏳ Move to next scraper (Investors)
5. ⏳ Build remaining 4 scrapers
6. ⏳ Create comprehensive output model
7. ⏳ Build report generation system

## Cost Notes

- **Free Tier:** 25 companies per run
- **Paid Plan:** Up to 6,640+ companies per run
- **Cost:** ~$15 per 1,000 companies (based on Apify pricing)

## Files Generated

- `yc_scraper_results_20251004_234716.json` - Full JSON data
- `yc_scraper_report_20251004_234716.txt` - Formatted text report
- `ANALYSIS.md` - This analysis document
