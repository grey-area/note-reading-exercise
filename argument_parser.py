import argparse


def validate_args(parser, args):
    if args.tempo < 10 or args.tempo > 180:
        parser.error("tempo should be between 10 and 180 (inclusive)")

    if args.num_exercises < 1 or args.num_exercises > 200:
        parser.error("num-execsises should be between 1 and 200 (inclusive)")

    if args.num_bars < 1 or args.num_bars > 6:
        parser.error("num-bars should be between 1 and 6 (inclusive)")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--tempo', type=int,
        default=45,
        help='Tempo'
    )
    parser.add_argument(
        '--num-exercises', type=int,
        default=10,
        help='Number of exercises'
    )
    parser.add_argument(
        '--num-bars', type=int,
        default=2,
        help='Number of bars per exercise'
    )

    args = parser.parse_args()
    validate_args(parser, args)

    return args
