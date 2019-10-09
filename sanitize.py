#!/usr/bin/env python3
"""Map 0."""

import sys
import re

lineNum = 0
for line in sys.stdin:
    if lineNum == 2:
        words = line.split()
        for word in words:
            word = re.sub(r'[^a-zA-Z]+', '', word)
            word = word.upper()
            # if ":" not in word:
            #     if "|" not in word:
            #         if "_" not in word:
            #             if "_" not in word:
            #                 if "." not in word:
            #                     if "#" not in word:
            #                         if not any(char.isdigit() for char in word):
            if word.isalpha():
                print(word + "\t1")
        lineNum = lineNum+1
    else:
        lineNum = lineNum+1
    if lineNum == 3:
        lineNum = 0