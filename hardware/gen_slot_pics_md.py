#!/usr/bin/env python3
"""
Usage: gen_slot_pics_md.py ../pics.yaml <card> <slot>

Generates a copy-pasteable Markdown snippet for the pictures of a card in a specific slot,
given the card name and slot.
The snippet includes the image thumbnail and the caption (as alt text and printed below the image),
and links to the full-size image.

"""

import sys
import yaml
import re

def generate_snippets(pics, card, slot):
    """
    Generates a list of Markdown snippets for the pictures of a card in a specific slot.

    Args:
        pics (dict): The loaded pics catalog from YAML.
        card (str): The card name.
        slot (str): The slot number as a string.

    Returns:
        list: A list of Markdown snippet strings.
    """
    thumb_url_gen = pics.get('thumb_url_gen', {})
    snippets = []

    for pic in pics['pics']:
        if pic.get('card') != card:
            continue

        slots = [str(s) for s in pic.get('slots', [])]
        if slot not in slots:
            continue

        caption = pic['caption']
        url = pic['url']
        thumb_url = re.sub(thumb_url_gen['match'], thumb_url_gen['replace'], url)
        md_snippet = f'{caption}:\n\n[![{caption}]({thumb_url})]({url})\n\n'
        snippets.append(md_snippet)

    return snippets

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: gen_slot_pics_md.py <yaml_path> <card> <slot>")
        sys.exit(1)

    yaml_path, card, slot = sys.argv[1:4]

    with open(yaml_path, 'r') as f:
        catalog = yaml.safe_load(f)
        snippets = generate_snippets(catalog, card, slot)
        for snippet in snippets:
            print(snippet)
