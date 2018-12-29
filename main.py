#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from datetime import datetime
from masterpiece import Masterpiece
from subprocess import check_output
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '--tempo', type=int,
    default=45,
    help='Tempo'
)
parser.add_argument(
    '--length', type=int,
    default=10,
    help='Number of exercises'
)
args = parser.parse_args()


if __name__ == "__main__":
    dtime = datetime.now()
    ans_time = time.mktime(dtime.timetuple())
    my_masterpiece = Masterpiece(
        rules_path="rules.json",
        length=args.length,
        tempo=args.tempo)
    subfolder = "output"
    os.makedirs(subfolder, exist_ok=True)
    lilypond_str = my_masterpiece.create_midi_file(f'{subfolder}/{ans_time}.mid')

    with open(f'{subfolder}/{ans_time}.txt', 'w') as f:
        f.write(lilypond_str)

    cmd_str = f'lilypond --output={subfolder}/{ans_time} {subfolder}/{ans_time}.txt'
    check_output(cmd_str.split(' '))
