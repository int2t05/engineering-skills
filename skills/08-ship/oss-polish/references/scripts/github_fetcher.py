"""
GitHub Fetcher - Fetch repository data from the GitHub API.
Uses the GitHub Search API to fetch repositories by topic.
"""
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from config import (
    GITHUB_TOKEN, TOPIC, GITHUB_API_BASE,
    GITHUB_PER_PAGE, GITHUB_MAX_PAGES, GITHUB_SEARCH_SORT,
    GITHUB_SEARCH_ORDER, FETCH_REQUEST_DELAY
)


class GitHubFetcher:
    """Fetch repository data from the GitHub API."""

    def __init__(self, token: str = None, topic: str = None):
        """
        Initialize.

        Args:
            token: GitHub Personal Access Token
            topic: GitHub Topic to search
        """
        self.token = token or GITHUB_TOKEN
        self.topic = topic or TOPIC
        self.api_base = GITHUB_API_BASE
        self.per_page = GITHUB_PER_PAGE
        self.max_pages = GITHUB_MAX_PAGES
        self.delay = FETCH_REQUEST_DELAY

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Topics-Trending/1.0"
        })

        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None

    def fetch(self, sort_by: str = None, limit: int = None) -> List[Dict]:
        """
        Fetch the list of repositories under the specified topic.

        Args:
            sort_by: Sort method (stars, forks, updated)
            limit: Maximum number of results

        Returns:
            [
                {
                    "rank": 1,
                    "repo_name": "owner/repo",
                    "owner": "owner",
                    "stars": 1000,
                    "forks": 100,
                    "issues": 10,
                    "language": "Python",
                    "url": "https://github.com/owner/repo",
                    "description": "...",
                    "topics": ["topic1", "topic2"],
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                },
                ...
            ]
        """
        sort_by = sort_by or GITHUB_SEARCH_SORT
        limit = limit or (self.per_page * self.max_pages)

        print(f"📡 Fetching repositories for topic '{self.topic}'...")
        print(f"   Sort by: {sort_by}")

        repos = []
        page = 1

        while page <= self.max_pages and len(repos) < limit:
            # Check rate limit
            if self.rate_limit_remaining < 10:
                self._wait_for_rate_limit()

            data = self._fetch_page(page, sort_by)

            if not data or "items" not in data:
                break

            items = data["items"]
            if not items:
                break

            for item in items:
                repo = self._parse_repo_item(item, len(repos) + 1)
                repos.append(repo)

                if len(repos) >= limit:
                    break

            # Update rate limit info
            self._update_rate_limit(data)

            print(f"   Page {page}: fetched {len(items)} repos (total {len(repos)})")

            # If fewer than per_page results, this is the last page
            if len(items) < self.per_page:
                break

            page += 1

            # Request delay
            if page <= self.max_pages and len(repos) < limit:
                time.sleep(self.delay)

        print(f"✅ Successfully fetched {len(repos)} repositories")
        return repos

    def _fetch_page(self, page: int, sort_by: str) -> Optional[Dict]:
        """
        Fetch a single page of results.

        Args:
            page: Page number
            sort_by: Sort method

        Returns:
            API response data
        """
        query = f"topic:{self.topic}"
        url = f"{self.api_base}/search/repositories"

        params = {
            "q": query,
            "sort": sort_by,
            "order": GITHUB_SEARCH_ORDER,
            "per_page": self.per_page,
            "page": page
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"   ⚠️ Request failed (page {page}): {e}")
            return None

    def _parse_repo_item(self, item: Dict, rank: int) -> Dict:
        """
        Parse repository data.

        Args:
            item: Repository item returned by the GitHub API
            rank: Rank

        Returns:
            Repository info dict
        """
        owner_data = item.get("owner") or {}
        owner = owner_data.get("login", "")
        name = item.get("name", "")
        repo_name = f"{owner}/{name}"

        return {
            "rank": rank,
            "repo_name": repo_name,
            "owner": owner,
            "name": name,
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "issues": item.get("open_issues_count", 0),
            "language": item.get("language", ""),
            "url": item.get("html_url", ""),
            "description": item.get("description", ""),
            "topics": item.get("topics", []),
            "created_at": item.get("created_at", ""),
            "updated_at": item.get("updated_at", ""),
            "pushed_at": item.get("pushed_at", ""),
            "homepage": item.get("homepage", ""),
            "archived": item.get("archived", False),
        }

    def _update_rate_limit(self, response_data: Dict):
        """
        Update rate limit info.

        Args:
            response_data: API response data
        """
        # Note: in actual requests this info comes from response headers
        # This is a simplified version
        pass

    def _wait_for_rate_limit(self):
        """Wait for rate limit to reset."""
        if self.rate_limit_reset:
            now = int(time.time())
            wait_time = self.rate_limit_reset - now + 1

            if wait_time > 0:
                print(f"⏳ Rate limit exhausted, waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

    def fetch_new_repos(self, days: int = 7) -> List[Dict]:
        """
        Fetch repositories created recently.

        Args:
            days: Number of recent days

        Returns:
            Repository list
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"topic:{self.topic} created:>{cutoff_date}"

        print(f"📡 Fetching repositories created in the last {days} days...")

        repos = []
        page = 1

        while page <= self.max_pages:
            url = f"{self.api_base}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": self.per_page,
                "page": page
            }

            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if not data or "items" not in data:
                    break

                items = data["items"]
                if not items:
                    break

                for item in items:
                    repo = self._parse_repo_item(item, len(repos) + 1)
                    repos.append(repo)

                print(f"   Page {page}: fetched {len(items)} repos")

                if len(items) < self.per_page:
                    break

                page += 1
                time.sleep(self.delay)

            except requests.RequestException as e:
                print(f"   ⚠️ Request failed: {e}")
                break

        print(f"✅ Fetched {len(repos)} new repositories")
        return repos

    def fetch_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Fetch detailed information for a single repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository details
        """
        url = f"{self.api_base}/repos/{owner}/{repo}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"   ⚠️ Failed to fetch repo details {owner}/{repo}: {e}")
            return None


def fetch_repos(sort_by: str = "stars", limit: int = 100) -> List[Dict]:
    """Convenience function: fetch repository list."""
    fetcher = GitHubFetcher()
    return fetcher.fetch(sort_by=sort_by, limit=limit)
