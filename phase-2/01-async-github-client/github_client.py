import argparse
import asyncio
import time

import httpx
import requests


def fetch_api(endpoint: str):
    try:
        response = requests.get(
            endpoint,
            timeout=5,
        )
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
        if remaining == 0:
            return {"error": "Rate limit reached. Try again later."}
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        data = response.json()

        return data

    except requests.exceptions.Timeout:
        return {"error": "Connection timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed"}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}


def get_profile(username: str):
    url = f"https://api.github.com/users/{username}"
    return fetch_api(url)


def get_repos(username: str):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=10"
    repos = fetch_api(url)
    if isinstance(repos, dict) and "error" in repos:
        return repos
    return sorted(repos, key=lambda r: r["pushed_at"], reverse=True)


def fetch_user_data(username: str) -> tuple[dict, list]:
    profile = get_profile(username)
    repos = get_repos(username)
    return profile, repos


async def async_fetch_api(client: httpx.AsyncClient, endpoint: str) -> dict:
    try:
        response = await client.get(endpoint, timeout=5)
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
        if remaining == 0:
            return {"error": "Rate limit reached. Try again later."}
        if response.status_code == 404:
            return {"error": "User not found"}
        response.raise_for_status()
        return response.json()
    except httpx.TimeoutException:
        return {"error": "Connection timeout"}
    except httpx.ConnectError:
        return {"error": "Connection failed"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e}"}


async def async_fetch_both(username: str) -> tuple[dict, list]:
    profile_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=10"

    async with httpx.AsyncClient() as client:
        profile, repos = await asyncio.gather(
            async_fetch_api(client, profile_url), async_fetch_api(client, repos_url)
        )
    return profile, repos


def print_summary(profile: dict, repos: list) -> None:
    if isinstance(profile, dict) and "error" in profile:
        print(f"Error fetching profile: {profile['error']}")
        return
    if isinstance(repos, dict) and "error" in repos:
        print(f"Error fetching repos: {repos['error']}")
        return
    print(f"""
====={profile.get("name") or "No name"}({profile["login"]})=====
{profile.get("bio") or "No bio"}
Followers: {profile["followers"]}
Public repo count: {profile["public_repos"]}
Last pushes:""")
    for repo in repos[:3]:
        print(f"{repo['name']} - {repo['pushed_at']}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Github user profile and recent repos concurrently"
    )
    parser.add_argument("username", help="Github username to look up")
    args = parser.parse_args()

    start = time.perf_counter()
    profile, repos = fetch_user_data(args.username)
    print_summary(profile, repos)
    sync_time = time.perf_counter() - start
    print(f"Sync: {sync_time:.3f}s")

    start = time.perf_counter()
    profile, repos = asyncio.run(async_fetch_both(args.username))
    print_summary(profile, repos)
    async_time = time.perf_counter() - start
    print(f"Async: {async_time:.3f}s")

    speedup = sync_time / async_time
    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    main()
