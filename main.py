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

chapters = []

for index, item in enumerate(book_items):
    plain_text = strip_html_tags(item.get_content())
    chapters.append({"filename": f"{source}_chapter_{index}", "plain_text": plain_text})

for chapter in chapters:
    print(f"Processing {chapter["filename"]}...")
    create_aiff(chapter["filename"], chapter["plain_text"])

for chapter in chapters:
    print(f"Converting {chapter["filename"]} to MP3...")
    convert_to_mp3(chapter["filename"])

print("Done")
