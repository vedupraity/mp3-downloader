import html
import os
import re

import ffmpeg


def clean_text(text: str) -> str:
    # unescape html/xml
    cleaned_text = html.unescape(text)

    # remove dirty characters that creates problem in windows filenames
    dirty_chars_map = {
        "\\": " ",
        "/": " ",
        ":": " ",
        "*": "#",
        "?": " ",
        '"': " ",
        "<": " ",
        ">": " ",
        "|": " I ",
    }
    for _k, _v in dirty_chars_map.items():
        cleaned_text = cleaned_text.replace(_k, _v)

    # remove non-utf8 chars
    utf8_chars = []
    for char in cleaned_text:
        try:
            char.encode("utf-8")
            utf8_chars.append(char)
        except UnicodeEncodeError:
            # Character is not UTF-8, replace it with an empty string
            utf8_chars.append("")
    cleaned_text = "".join(utf8_chars)

    # remove extra whitespaces
    cleaned_text = " ".join([_.strip() for _ in cleaned_text.split(" ") if _])

    # fix brackets
    re_patterns_map = {
        "\s+\)": ")",
        "\(\s+": "(",
        "\s+\]": "]",
        "\[\s+": "[",
    }
    for _k, _v in re_patterns_map.items():
        cleaned_text = re.sub(_k, _v, cleaned_text)

    return cleaned_text


def convert_to_mp3(
    input_path: str, output_path: str, delete_original: bool = True
) -> None:
    ffmpeg.input(input_path).output(output_path, audio_bitrate="320k").run(
        overwrite_output=True
    )

    if delete_original:
        os.remove(input_path)
