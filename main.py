#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from subprocess import check_output
from masterpiece import Masterpiece
from argument_parser import parse_args


if __name__ == '__main__':
    args = parse_args()

    result_dir = 'output'
    os.makedirs(result_dir, exist_ok=True)
    filename_str = os.path.join(result_dir, f'{time.time():.01f}')

    with open('rules.json') as f:
        rules = json.load(f)
    rhythm = [[0.5] * (4 * args.num_bars - 1) + [4.5]]

    my_masterpiece = Masterpiece(rules, rhythm, args)
    lilypond_str = my_masterpiece.create_midi_file(f'{filename_str}.mid')

    with open(f'{filename_str}.txt', 'w') as f:
        f.write(lilypond_str)

    cmd_str = 'lilypond --output={0} {0}.txt'.format(filename_str)
    check_output(cmd_str.split(' '))
