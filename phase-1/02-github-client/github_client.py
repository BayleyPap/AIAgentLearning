import requests

USERNAME = "BayleyPap"
PROFILEURL = f"https://api.github.com/users/{USERNAME}"
REPOURL = f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=10"


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


def get_profile():
    return fetch_api(PROFILEURL)


def get_repos():
    repos = fetch_api(REPOURL)
    if isinstance(repos, dict) and "error" in repos:
        return repos
    return sorted(repos, key=lambda r: r["pushed_at"], reverse=True)


def print_summary():
    profile = get_profile()
    repos = get_repos()
    if "error" in repos:
        print(f"Error: {repos['error']}")
        return
    print(f"""
====={profile["name"]}({profile["login"]})=====
{profile["bio"]}
Followers: {profile["followers"]}
Public repo count: {profile["public_repos"]}
Last pushes:""")
    for repo in repos[:3]:
        print(f"{repo['name']} - {repo['pushed_at']}")


if __name__ == "__main__":
    print_summary()
