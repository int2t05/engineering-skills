"""
Config module - GitHub Topics Trending configuration.
"""
import os

# ============================================================================
# GitHub API configuration
# ============================================================================
GITHUB_TOKEN = os.getenv("GH_TOKEN")
TOPIC = os.getenv("TOPIC")
GITHUB_API_BASE = "https://api.github.com"
GITHUB_PER_PAGE = 100  # GitHub API max per page
GITHUB_MAX_PAGES = 10  # Maximum pages to fetch (1000 repos)

# GitHub search configuration
GITHUB_SEARCH_SORT = "stars"  # stars, forks, updated
GITHUB_SEARCH_ORDER = "desc"  # desc, asc

# ============================================================================
# Request configuration
# ============================================================================
FETCH_REQUEST_DELAY = 0.5  # API request delay (seconds)


def format_number(num: int) -> str:
    """Format number for display."""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    return str(num)


def get_repo_url(owner: str, repo_name: str) -> str:
    """Generate repository URL."""
    return f"https://github.com/{owner}/{repo_name}"
