from io import BytesIO
import os

from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from PIL import Image
import requests
import yt_dlp

from config.settings import Settings
from utils.file_operations import clean_text


class YouTube:

    def update_meta_info_of_song(self, context: dict):
        if context["status"] == "finished" and context["postprocessor"] == "Metadata":
            song_dir = context["info_dict"]["__finaldir"]
            saved_song_path = context["info_dict"]["filepath"]
            new_song_name = clean_text(context["info_dict"]["title"]) + ".mp3"

            if os.path.exists(saved_song_path):
                if os.path.exists(os.path.join(song_dir, new_song_name)):
                    os.remove(os.path.join(song_dir, new_song_name))

                os.rename(
                    saved_song_path,
                    os.path.join(song_dir, new_song_name),
                )

                thumbnail_url = context["info_dict"]["thumbnail"]

                response = requests.get(thumbnail_url)

                image = Image.open(BytesIO(response.content))
                width, height = image.size

                if width > height:
                    left = (width - height) / 2
                    right = left + height
                    image = image.crop((left, 0, right, height))
                elif height > width:
                    top = (height - width) / 2
                    bottom = top + width
                    image = image.crop((0, top, width, bottom))

                if width > 500 or height > 500:
                    image = image.resize((500, 500))

                image_buffer = BytesIO()
                image.save(image_buffer, format="JPEG")
                image_buffer.seek(0)

                mp3_file_path = os.path.join(song_dir, new_song_name)
                audio = MP3(mp3_file_path, ID3=ID3)

                audio.tags.add(
                    APIC(
                        mime="image/jpeg",
                        type=3,  # Cover type
                        desc="Cover",
                        data=image_buffer.read(),
                    )
                )

                audio.save()

    def download_and_save_song(self, song_url: str, output_dir_path: str):
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                },
                {"key": "FFmpegMetadata"},
            ],
            "ignoreerrors": True,
            "postprocessor_hooks": [self.update_meta_info_of_song],
            "outtmpl": output_dir_path + "/%(id)s.%(ext)s",
            "cookiefile": Settings.YOUTUBE_COOKIES_FILE,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song_url])
