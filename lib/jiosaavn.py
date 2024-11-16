import requests


SAAVN_API_HEADERS = {
    "authority": "saavn.dev",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en-GB;q=0.9,en;q=0.8,hi;q=0.7,en-IN;q=0.6",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://saavn.dev/docs",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
}

def search_songs(query: str):
    url = "https://saavn.dev/api/search/songs"
    headers = SAAVN_API_HEADERS
    params = {"query": query, "limit": 10}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"Error while fetching results by query: {query}")
        print(f"HTTP {response.status_code}")
        print(response.text)
        return []

    response_data = response.json()["data"]
    response_data['results'][0]

