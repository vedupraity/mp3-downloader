import requests
from config.logger import get_logger


logger = get_logger(__name__)


class JioSaavn:
    def __init__(self) -> None:
        self.SAAVN_API_HEADERS = {
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

    def search_songs(self, query: str) -> list:
        """
        Search for songs based on the provided query.

        API reference:
            https://saavn.dev/docs#tag/search/GET/api/search/songs

        Returns:
            Array of song details
        """
        url = "https://saavn.dev/api/search/songs"
        headers = self.SAAVN_API_HEADERS
        params = {"query": query, "limit": 10}
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error while fetching results by query: {query}")
            logger.error(f"HTTP {response.status_code}")
            logger.error(response.text)
            return []

        response_data = response.json()["data"]
        response_data["results"][0]

    def get_song_info_by_url(self, song_url) -> object:
        """
        Retrieve song by direct link to the song on JioSaavn.

        API reference:
            https://saavn.dev/docs#tag/songs/GET/api/songs

        Returns:
            Song details
        """
        url = "https://saavn.dev/api/songs"
        headers = self.SAAVN_API_HEADERS
        params = {"link": song_url}

        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error while fetching by song url: {song_url}")
            logger.error(f"HTTP {response.status_code}")
            logger.error(response.text)
            return None

        search_results = response.json()["data"]

        return search_results[0]
