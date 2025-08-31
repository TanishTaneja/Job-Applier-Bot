import requests
import json

GRAPHQL_BASE_URL = "https://e5mquma77feepi2bdn4d6h3mpu.appsync-api.us-east-1.amazonaws.com/graphql"
session = requests.Session()
session.headers.update({'Connection': 'keep-alive'})


def set_graphql_headers():
    return {
        "Content-Type": "application/json",
        "authorization": "Bearer Status|unauthenticated|Session|",
        "referer": "https://hiring.amazon.ca",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "country": "Canada",
    }


def make_graphql_request(query: str, variables: dict = None):
    payload = {
        "query": query,
        "variables": variables or {}
    }

    headers = set_graphql_headers()

    response = session.post(
        GRAPHQL_BASE_URL,
        data=json.dumps(payload),
        headers=headers,
        timeout=15  # optional timeout
    )

    return response.json()