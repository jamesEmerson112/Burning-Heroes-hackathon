"""Module defines Pydantic models for this project.

These models are used mainly for the structured tool and LLM outputs.
Resources:
- https://docs.pydantic.dev/latest/concepts/models/
"""

from __future__ import annotations

from pydantic import BaseModel


class InstagramPost(BaseModel):
    """Instagram Post Pydantic model.

    Returned as a structured output by the `tool_scrape_instagram_profile_posts` tool.

    url: The URL of the post.
    likes: The number of likes on the post.
    comments: The number of comments on the post.
    timestamp: The timestamp when the post was published.
    caption: The post caption.
    alt: The post alt text.
    """

    url: str
    likes: int
    comments: int
    timestamp: str
    caption: str | None = None
    alt: str | None = None


class AgentStructuredOutput(BaseModel):
    """Structured output for the ReAct agent.

    Returned as a structured output by the ReAct agent.

    total_likes: The total number of likes on the most popular posts.
    total_comments: The total number of comments on the most popular posts.
    most_popular_posts: A list of the most popular posts.
    """

    total_likes: int
    total_comments: int
    most_popular_posts: list[InstagramPost]


# ============================================================================
# Y Combinator Scraper Models
# ============================================================================

class YCFounder(BaseModel):
    """Y Combinator founder information.

    Attributes:
        id: Founder ID in YC database
        name: Full name of founder
        linkedin: LinkedIn profile URL (optional)
    """
    id: int
    name: str
    linkedin: str | None = None


class YCJob(BaseModel):
    """Y Combinator job posting.

    Attributes:
        id: Job ID
        title: Job title
        description: Job description (optional)
        location: Job location (optional)
    """
    id: int
    title: str
    description: str | None = None
    location: str | None = None


class YCCompany(BaseModel):
    """Y Combinator company profile.

    Attributes:
        company_id: YC company ID
        company_name: Name of the company
        batch: YC batch (e.g., "Winter 2025", "Summer 2024")
        short_description: Brief company description
        long_description: Detailed company description
        founders: List of company founders
        team_size: Team size (as string or int)
        tags: List of industry/category tags
        company_location: Geographic location
        website: Company website URL
        url: YC company profile URL
        open_jobs: List of open job postings
        is_hiring: Whether company is actively hiring
        company_linkedin: Company LinkedIn URL
        status: Company status (e.g., "ACTIVE")
        year_founded: Year company was founded
    """
    company_id: int
    company_name: str
    batch: str | None = None
    short_description: str | None = None
    long_description: str | None = None
    founders: list[YCFounder] = []
    team_size: int | str | None = None
    tags: list[str] = []
    company_location: str | None = None
    website: str | None = None
    url: str | None = None
    open_jobs: list[YCJob] = []
    is_hiring: bool = False
    company_linkedin: str | None = None
    status: str | None = None
    year_founded: int | None = None
