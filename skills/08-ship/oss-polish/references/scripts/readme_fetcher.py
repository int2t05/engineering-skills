"""
README Fetcher - Fetch repository README content.
Uses the GitHub API to fetch a repository's README file.
"""
import time
import re
import requests
from typing import Dict, List, Optional

from config import GITHUB_TOKEN, GITHUB_API_BASE, FETCH_REQUEST_DELAY


class ReadmeFetcher:
    """Fetch repository README content."""

    def __init__(self, token: str = None):
        """
        Initialize.

        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or GITHUB_TOKEN
        self.api_base = GITHUB_API_BASE
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

    def fetch_readme(self, owner: str, repo: str, html: bool = False) -> Optional[str]:
        """
        Fetch repository README content.

        Args:
            owner: Repository owner
            repo: Repository name
            html: Whether to return HTML format

        Returns:
            README content
        """
        url = f"{self.api_base}/repos/{owner}/{repo}/readme"

        if html:
            self.session.headers["Accept"] = "application/vnd.github.html"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # GitHub returns base64-encoded content
            data = response.json()

            if data.get("encoding") == "base64":
                import base64
                content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="ignore")
                return content
            else:
                return data.get("content", "")

        except requests.RequestException as e:
            print(f"   ⚠️ Failed to fetch README {owner}/{repo}: {e}")
            return None

    def fetch_readme_summary(self, owner: str, repo: str, max_length: int = 500) -> Optional[str]:
        """
        Fetch a README summary.

        Args:
            owner: Repository owner
            repo: Repository name
            max_length: Maximum length

        Returns:
            README summary text
        """
        readme = self.fetch_readme(owner, repo)

        if not readme:
            return None

        # Strip Markdown markup, extract plain text
        summary = self._extract_text_from_markdown(readme)

        # Truncate to the specified length
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(" ", 1)[0] + "..."

        return summary

    def _extract_text_from_markdown(self, markdown: str) -> str:
        """
        Extract plain text from Markdown.

        Args:
            markdown: Markdown content

        Returns:
            Plain text
        """
        # Remove code blocks
        markdown = re.sub(r'```.*?```', '', markdown, flags=re.DOTALL)
        markdown = re.sub(r'`.*?`', '', markdown)

        # Remove links
        markdown = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', markdown)

        # Remove images
        markdown = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', markdown)

        # Remove heading markers
        markdown = re.sub(r'^#+\s+', '', markdown, flags=re.MULTILINE)

        # Remove bold/italic
        markdown = re.sub(r'\*\*([^*]+)\*\*', r'\1', markdown)
        markdown = re.sub(r'\*([^*]+)\*', r'\1', markdown)
        markdown = re.sub(r'__([^_]+)__', r'\1', markdown)
        markdown = re.sub(r'_([^_]+)_', r'\1', markdown)

        # Remove horizontal rules
        markdown = re.sub(r'^---+$', '', markdown, flags=re.MULTILINE)
        markdown = re.sub(r'^\*\*\*+$', '', markdown, flags=re.MULTILINE)

        # Remove excess blank lines
        lines = [line.strip() for line in markdown.split('\n')]
        lines = [line for line in lines if line]

        return ' '.join(lines)

    def batch_fetch_readmes(self, repos: List[Dict], delay: float = None) -> Dict[str, str]:
        """
        Batch-fetch README content.

        Args:
            repos: Repository list
            delay: Request delay

        Returns:
            {repo_name: readme_summary} dict
        """
        delay = delay if delay is not None else self.delay
        summaries = {}

        print(f"📥 Starting batch README fetch...")

        for i, repo in enumerate(repos, 1):
            repo_name = repo.get("repo_name") or repo.get("name", "")

            if not repo_name or "/" not in repo_name:
                continue

            owner, name = repo_name.split("/", 1)

            print(f"  [{i}/{len(repos)}] {repo_name}")

            summary = self.fetch_readme_summary(owner, name)
            if summary:
                summaries[repo_name] = summary

            # Request delay
            if i < len(repos):
                time.sleep(delay)

        print(f"✅ Successfully fetched {len(summaries)} README summaries")
        return summaries

    def fetch_from_github_raw(self, owner: str, repo: str, branch: str = "main") -> Optional[str]:
        """
        Fetch README directly from GitHub raw content.

        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name

        Returns:
            README content
        """
        # Try common README file names
        readme_names = ["README.md", "README.markdown", "README.rst", "README.txt"]

        for name in readme_names:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}"

            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except requests.RequestException:
                continue

        # Try master branch
        if branch == "main":
            return self.fetch_from_github_raw(owner, repo, "master")

        return None


def fetch_readme_summary(owner: str, repo: str) -> Optional[str]:
    """Convenience function: fetch README summary."""
    fetcher = ReadmeFetcher()
    return fetcher.fetch_readme_summary(owner, repo)


def batch_fetch_readmes(repos: List[Dict]) -> Dict[str, str]:
    """Convenience function: batch-fetch READMEs."""
    fetcher = ReadmeFetcher()
    return fetcher.batch_fetch_readmes(repos)
