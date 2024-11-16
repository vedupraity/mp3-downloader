import html
import os

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import requests

from config.logger import get_logger
from utils.file_operations import clean_text, convert_to_mp3


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

    def get_artist_info(self, artist_url: str):
        url = "https://saavn.dev/api/artists"
        headers = self.SAAVN_API_HEADERS

        params = {"link": artist_url, "songCount": 1, "albumCount": 1}

        response = requests.get(url, params=params, headers=headers)
        return response.json()["data"]

    def update_meta_info_of_song(self, mp3_file_path: str, song_info: dict):
        audio = EasyID3(mp3_file_path)
        audio["title"] = html.unescape(song_info["name"])
        artists = "; ".join(
            [html.unescape(_["name"]) for _ in song_info["artists"]["primary"]]
            + [html.unescape(_["name"]) for _ in song_info["artists"]["featured"]]
        )
        audio["artist"] = artists
        audio["composer"] = artists
        audio["album"] = html.unescape(song_info["album"]["name"])
        audio["date"] = str(song_info["year"])
        audio["organization"] = html.unescape(song_info["label"])
        audio["copyright"] = html.unescape(song_info["copyright"])
        audio["language"] = html.unescape(song_info["language"])
        audio.save()

        audio = MP3(mp3_file_path, ID3=ID3)
        response = requests.get(
            list(filter(lambda d: d["quality"] == "500x500", song_info["image"]))[0][
                "url"
            ]
        )

        image_content = response.content

        try:
            if "error" in image_content.decode().lower():
                artist_info = self.get_artist_info(
                    song_info["artists"]["primary"][0]["url"]
                )
                response = requests.get(
                    list(
                        filter(
                            lambda d: d["quality"] == "500x500", artist_info["image"]
                        )
                    )[0]["url"]
                )
                image_content = response.content

                try:
                    if "error" in image_content.decode().lower():
                        image_content = None
                except:
                    pass

        except:
            pass

        if image_content:
            audio.tags.add(
                APIC(mime="image/jpeg", type=3, desc="Cover", data=image_content)
            )
            audio.save()

    def download_and_save_song(self, song_info: dict, output_dir_path: str):
        mp4_file_name = clean_text(f"{song_info['name']}.mp4")
        mp4_file_path = os.path.join(output_dir_path, mp4_file_name)
        mp3_file_name = clean_text(f"{song_info['name']}.mp3")
        mp3_file_path = os.path.join(output_dir_path, mp3_file_name)

        if os.path.exists(mp3_file_path):
            return

        url = list(
            filter(lambda d: d["quality"] == "320kbps", song_info["downloadUrl"])
        )[0]["url"]
        response = requests.get(url)

        with open(mp4_file_path, "wb") as f:
            f.write(response.content)

        convert_to_mp3(
            mp4_file_path,
            mp3_file_path,
        )

        self.update_meta_info_of_song(mp3_file_path, song_info)
