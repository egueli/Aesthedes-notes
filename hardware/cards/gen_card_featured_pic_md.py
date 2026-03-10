#!/usr/bin/env python3
"""
Usage: gen_card_featured_pic_md.py ../pics.yaml <card>

Generates a copy-pasteable Markdown snippet for the featured picture of a card, given the card name.
The featured picture is the one with the "featured: true" flag in the referenced pics.yaml file.
The snippet includes the image thumbnail and the caption, and links to the full-size image.

"""

import sys
import yaml
import re

with open(sys.argv[1], 'r') as f:
    pics = yaml.safe_load(f)

thumb_url_gen = pics.get('thumb_url_gen', {})

card = sys.argv[2]

for pic in pics['pics']:
    if pic['card'] == card and pic.get('featured'):
        caption = pic['caption']
        url = pic['url']
        thumb_url = re.sub(thumb_url_gen['match'], thumb_url_gen['replace'], url)
        md_snippet = f'[![{caption}]({thumb_url})]({url})\n\n{caption}\n\n'
        print(md_snippet)
        break