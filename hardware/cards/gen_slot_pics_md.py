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

with open(sys.argv[1], 'r') as f:
    pics = yaml.safe_load(f)

thumb_url_gen = pics.get('thumb_url_gen', {})

card = sys.argv[2]
slot = int(sys.argv[3])

for pic in pics['pics']:
    if pic.get('card') == card and slot in pic.get('slots', []):
        caption = pic['caption']
        url = pic['url']
        thumb_url = re.sub(thumb_url_gen['match'], thumb_url_gen['replace'], url)
        md_snippet = f'{caption}:\n\n[![{caption}]({thumb_url})]({url})\n\n'
        print(md_snippet)
