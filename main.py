#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from subprocess import check_output
from masterpiece import Masterpiece
from argument_parser import parse_args


if __name__ == "__main__":
    time_str = f'{time.time():.01f}'
    args = parse_args()

    with open('rules.json') as f:
        rules = json.load(f)
    rules['rhythm'] = [[0.5] * (4 * args.num_bars - 1) + [4.5]]

    my_masterpiece = Masterpiece(
        rules=rules,
        length=args.num_exercises,
        tempo=args.tempo)
    subfolder = "output"
    os.makedirs(subfolder, exist_ok=True)
    lilypond_str = my_masterpiece.create_midi_file(f'{subfolder}/{time_str}.mid')

    with open(f'{subfolder}/{time_str}.txt', 'w') as f:
        f.write(lilypond_str)

    cmd_str = f'lilypond --output={subfolder}/{time_str} {subfolder}/{time_str}.txt'
    check_output(cmd_str.split(' '))
