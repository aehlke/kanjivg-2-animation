# !/usr/bin/env python

from __future__ import (
    print_function,
    unicode_literals,
)

import math
import os
import sys
from io import open

from svg.path import parse_path
from tqdm import tqdm


# A function that allows you to retrieve a string between two specified strings
def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


KANJIVG_SVG_DIR = './kanjivg/kanji/'


# Iterate through each svg file in the kanjivg directory.
for filename in tqdm(os.listdir(KANJIVG_SVG_DIR),
                     mininterval=5, miniters=10):
    # Our source and target files and directories
    source_file = open(KANJIVG_SVG_DIR + filename, 'r', encoding='utf8')
    target_file = open('./converted/{}-animated.svg'.format(filename[:-4]),
                       'w+', encoding='utf8')

    # The array that we will use to build the various parts comprising the svg
    svg_build_array = []

    # The array that will contain all values of 'd' (the path code) in the original svg file
    dpath = []

    # Retrieve the value of 'd' (the path code) in the original svg file
    for line in source_file:
        if '<path' in line and 'd="' in line:
            dpath.append(find_between(line, ' d="', '\/>'))

    source_file.close()

    # Start building an array that contains the fragments of our svg
    svg_build_array.append(
        '<svg id="kvg-{}" class="kanjivg" width="106" height="126" '.format(
            filename[:-4]))

    # Thought: maybe make end animation last longer before repeat? Or maybe keep it permanent?

    # Begin defining the svg, its components and their styles
    svg_build_array.append("""xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" version="1.1" baseProfile="full"><defs><style type="text/css"><![CDATA[path.black{fill:none;stroke:black;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}path.grey{fill:none;stroke:# ddd;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}path.stroke{fill:none;stroke:black;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}]]></style></defs>""")

    # First we draw the grey kanji strokes in the background, without any animations
    for a in dpath:
        svg_build_array.append('<path d="' + a + '" class="grey" />')

    # The value of i represents
    i = 0.0

    # Then we handle the black kanji strokes, which will be animated in the foreground
    for b in dpath:
        path_length = parse_path(b).length()
        stroke_length = 150

        # Change the stroke length if the path length exceeds our expectations
        if path_length > 150 and path_length < 200:
            stroke_length = 200
        elif path_length > 200  and path_length < 250:
            stroke_length = 250
        elif path_length > 250:
            stroke_length = 300

        # Begin handling the path
        svg_build_array.append(
            '<path d="{}" class="stroke" stroke-dasharray="{}">'.format(
                b, stroke_length))

        # Hide the black stroke for a specified duration ("dur")
        if i is not 0:
            svg_build_array.append(
                '<set attributeName="opacity" to="0" dur="{}s" />'.format(i))

        # Animate the black stroke after a specified duration (begin)
        svg_build_array.append(
            '<animate attributeName="stroke-dashoffset" from="{}" to="0" dur="1.8s" begin="{}s" fill="freeze" />'.format(
                stroke_length, i))

        # Finish handling the path
        svg_build_array.append('</path>')

        # Given the length of the current path, calculate the amount of time
        # we should add to 'i'. The next path will animate after that time.
        MIN_DELAY = 0.3
        MAX_DELAY = 1.0
        SHORT_PATH_LENGTH = 20
        LONG_PATH_LENGTH = 110
        i = (
            MIN_DELAY +
            min(0, (path_length - SHORT_PATH_LENGTH) / LONG_PATH_LENGTH) *
            (MAX_DELAY - MIN_DELAY)
        )

    # Finish handling the svg
    svg_build_array.append('</svg>')

    # Write the svg build array to a file
    for item in svg_build_array:
        target_file.write(item)

    # Close the file
    target_file.close()

# When the script is finished converting all files in the specified directory,
# it will print the following message to indicate it has finished.
print("Done.")
