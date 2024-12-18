import httpx

from prefect import flow, task # Prefect flow and task decorators

# Source for the code to deploy (here, a GitHub repo)
SOURCE_REPO="https://github.com/minyeong-jeong/prefect-test-flow.git"

@flow(log_prints=True)
def show_stars(github_repos: list[str] = ["PrefectHQ/prefect", "pydantic/pydantic", "huggingface/transformers"]):
    """Flow: Show the number of stars that GitHub repos have"""

    for repo in github_repos:
        # Call Task 1
        repo_stats = fetch_stats(repo)

        # Call Task 2
        stars = get_stars(repo_stats)

        # Print the result
        print(f"{repo}: {stars} stars")


@task
def fetch_stats(github_repo: str):
    """Task 1: Fetch the statistics for a GitHub repo"""

    return httpx.get(f"https://api.github.com/repos/{github_repo}").json()


@task
def get_stars(repo_stats: dict):
    """Task 2: Get the number of stars from GitHub repo statistics"""

    return repo_stats['stargazers_count']


# Run the flow
if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="test.py:show_stars",
    ).deploy(
        name="blabla",
        work_pool_name="4d-windows-pool",
    )

