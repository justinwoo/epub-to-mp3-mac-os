#!/usr/bin/env python3

import ebooklib
from ebooklib import epub
import re
import os
import argparse


def strip_html_tags(html_content):
    clean_text = re.sub(r"<[^>]+>", "", html_content.decode("utf-8"))
    return clean_text


os.system("mkdir -p temp")
os.system("mkdir -p output")


def create_aiff(filename, text):
    aiff_path = f"temp/{filename}.aiff"
    if not os.path.exists(aiff_path):
        print(f"Creating AIFF file: {aiff_path}")
        os.system(f'say -r 220 "{text}" -o "{aiff_path}"')
    else:
        print(f"AIFF file already exists: {aiff_path}")


def convert_to_mp3(filename):
    aiff_path = f"temp/{filename}.aiff"
    mp3_path = f"output/{filename}.mp3"
    if not os.path.exists(mp3_path):
        print(f"Converting to MP3: {mp3_path}")
        os.system(f'ffmpeg -i "{aiff_path}" "{mp3_path}"')
    else:
        print(f"MP3 file already exists: {mp3_path}")


parser = argparse.ArgumentParser(description="Process an EPUB file.")
parser.add_argument("file", help="Path to the EPUB file")
args = parser.parse_args()

source = os.path.basename(args.file)

book = epub.read_epub(args.file)
book_items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
print(f"Number of book items: {len(book_items)}")

parts = []

for index, item in enumerate(book_items):
    plain_text = strip_html_tags(item.get_content())
    words = plain_text.split()
    count = len(words)
    if count < 4000:
        parts.append(
            {"filename": f"{source}_chapter_{index}", "plain_text": plain_text}
        )
    else:
        for i in range(0, count, 4000):
            part_words = words[i : i + 4000]
            part_text = " ".join(part_words)
            parts.append(
                {
                    "filename": f"{source}_chapter_{index}_part_{i // 4000 + 1}",
                    "plain_text": part_text,
                }
            )

for part in parts:
    print(
        f"Processing {part["filename"]}, word count: {len(part["plain_text"].split())}"
    )
    create_aiff(part["filename"], part["plain_text"])

for part in parts:
    print(f"Converting {part["filename"]} to MP3...")
    convert_to_mp3(part["filename"])

print("Done")
