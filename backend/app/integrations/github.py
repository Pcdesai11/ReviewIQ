import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


class GitHubClient:
    def __init__(self) -> None:
        self._token = settings.github_token
        self._base = settings.github_api_base.rstrip("/")

    @property
    def available(self) -> bool:
        return bool(self._token)

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _get(self, path: str) -> Any:
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(f"{self._base}{path}", headers=self._headers())
            resp.raise_for_status()
            return resp.json()

    def _get_text(self, path: str, accept: str) -> str:
        headers = self._headers()
        headers["Accept"] = accept
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(f"{self._base}{path}", headers=headers)
            resp.raise_for_status()
            return resp.text

    def _post(self, path: str, body: dict) -> Any:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(f"{self._base}{path}", headers=self._headers(), json=body)
            resp.raise_for_status()
            return resp.json()

    def get_pull_request(self, owner: str, repo: str, number: int) -> dict:
        return self._get(f"/repos/{owner}/{repo}/pulls/{number}")

    def get_pull_diff(self, owner: str, repo: str, number: int) -> str:
        return self._get_text(
            f"/repos/{owner}/{repo}/pulls/{number}",
            accept="application/vnd.github.diff",
        )

    def create_issue_comment(self, owner: str, repo: str, number: int, body: str) -> dict | None:
        if not self.available:
            logger.info("Skipping PR comment — GITHUB_TOKEN not set")
            return None
        return self._post(f"/repos/{owner}/{repo}/issues/{number}/comments", {"body": body})

    def get_workflow_run(self, owner: str, repo: str, run_id: int) -> dict:
        return self._get(f"/repos/{owner}/{repo}/actions/runs/{run_id}")

    def get_workflow_run_logs_url(self, owner: str, repo: str, run_id: int) -> str | None:
        try:
            data = self._get(f"/repos/{owner}/{repo}/actions/runs/{run_id}/logs")
            return data if isinstance(data, str) else None
        except httpx.HTTPStatusError:
            return None

    def download_workflow_logs(self, owner: str, repo: str, run_id: int) -> str:
        """Best-effort log text from workflow run jobs."""
        if not self.available:
            return ""
        try:
            jobs = self._get(f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs")
            snippets: list[str] = []
            for job in jobs.get("jobs", []):
                snippets.append(job.get("name", ""))
                for step in job.get("steps", []):
                    if step.get("conclusion") == "failure":
                        snippets.append(f"{step.get('name')}: {step.get('conclusion')}")
            return "\n".join(snippets)
        except Exception as exc:
            logger.warning("Could not fetch workflow logs: %s", exc)
            return ""

    def list_check_runs(self, owner: str, repo: str, ref: str) -> list[dict]:
        if not self.available:
            return []
        try:
            data = self._get(f"/repos/{owner}/{repo}/commits/{ref}/check-runs")
            return data.get("check_runs", [])
        except Exception:
            return []


github_client = GitHubClient()
