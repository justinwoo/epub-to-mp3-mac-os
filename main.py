#!/usr/bin/env python3

import ebooklib
from ebooklib import epub
import re
import os
import argparse


def strip_html_tags(html_content):
    # lol
    clean_text = re.sub(r"<[^>]+>", "", html_content.decode("utf-8"))
    return clean_text


os.system("mkdir -p temp")
os.system("mkdir -p output")


def text_to_mp3(filename, text):
    os.system(f'say -r 220 "{text}" -o "temp/{filename}.aiff"')
    os.system(f'ffmpeg -i "temp/{filename}.aiff" "output/{filename}.mp3"')


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
    chapters.append({"index": index, "plain_text": plain_text})

for chapter in chapters:
    filename = f"{source}_chapter_{chapter['index']}"
    print("Turning into mp3:", filename)
    text_to_mp3(filename, chapter["plain_text"])

print("Done")
