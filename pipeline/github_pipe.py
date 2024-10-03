import logging
import os
from abc import ABC, abstractmethod
from typing import TypedDict

from github.PullRequest import PullRequest

from model.tinyllama import OllamaModel

from github import Github as GithubIntegration
from github.File import File
from github.GithubException import GithubException
from github.PaginatedList import PaginatedList

ACCESS_TOKEN = "ACTION_ACCESS_TOKEN"
REPO_OWNER = "REPOSITORY_OWNER"
REPO_NAME = "REPOSITORY_NAME"
PR_NUMBER = "PULL_REQUEST_NUMBER"


class PlatformRepositoryInfoParams(TypedDict):
    owner: str
    repo_name: str
    pr_number: int


class PlatformRepositoryProperties(TypedDict):
    files: PaginatedList[File]
    pull_request: PullRequest


class Platform(ABC):
    @abstractmethod
    def review(self):
        pass


class Github(Platform):
    def __init__(self, model: OllamaModel):
        self.model = model

    def review(self) -> None:
        token = self.get_token()
        repo_info = self.get_repo_info()
        pull_request_properties = self.get_pr_properties(token, repo_info)

        for file in pull_request_properties["files"]:
            try:
                with open(file.filename, "r") as f:
                    file_content = f.read()
            except FileNotFoundError as e:
                logging.warning(f"Failed to read file {file.filename}: {e}")
                continue

            try:
                result = self.model.generateChain(file_content)
            except Exception as e:
                logging.error(f"Failed to process file {file.filename} with model: {e}")
                return

            comment_body = f"Review for {file.filename}:\n\n{result}"
            try:
                pull_request_properties["pull_request"].create_issue_comment(
                    comment_body
                )
            except GithubException as e:
                logging.error(f"Failed to create comment for file {file.filename}: {e}")
                return

    def get_token(self) -> str:
        token = os.getenv(ACCESS_TOKEN)
        if not token:
            raise ValueError(
                f"{ACCESS_TOKEN} environment variable must be set in repository settings"
            )

        return token

    def get_repo_info(self) -> PlatformRepositoryInfoParams:
        owner = os.getenv(REPO_OWNER, "")
        if owner == "":
            raise ValueError(f"{REPO_OWNER} environment variable must be set")

        repo_name = os.getenv(REPO_NAME, "")
        if repo_name == "":
            raise ValueError(f"{REPO_NAME} environment variable must be set")

        pr_number = os.getenv(PR_NUMBER)
        if not pr_number:
            raise ValueError(f"{PR_NUMBER} environment variable must be set")

        try:
            pr_number = int(pr_number)
        except ValueError:
            raise ValueError(f"{PR_NUMBER} should be a valid integer")

        return {"owner": owner, "pr_number": pr_number, "repo_name": repo_name}

    def get_pr_properties(
        self, token: str, repo_info: PlatformRepositoryInfoParams
    ) -> PlatformRepositoryProperties:
        owner = repo_info["owner"]
        repo_name = repo_info["repo_name"]
        pr_number = repo_info["pr_number"]

        g = GithubIntegration(token)
        repo = g.get_repo(f"{owner}/{repo_name}")

        try:
            pull_request = repo.get_pull(pr_number)
            files = pull_request.get_files()

            return {"files": files, "pull_request": pull_request}
        except GithubException as e:
            raise RuntimeError(f"Failed to retrieve pull request properties: {e}")
