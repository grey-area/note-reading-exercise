import argparse


def validate_args(parser, args):
    if args.tempo < 10 or args.tempo > 180:
        parser.error('tempo should be between 10 and 180 (inclusive)')

    if args.num_exercises < 1 or args.num_exercises > 200:
        parser.error('num-execsises should be between 1 and 200 (inclusive)')

    if args.num_bars < 1 or args.num_bars > 6:
        parser.error('num-bars should be between 1 and 6 (inclusive)')

    args.key = args.key.lower()
    if args.key[0] not in 'abcdefg' or len(args.key) not in [1, 3] or (len(args.key) == 3 and args.key[1:] not in ['is', 'es']):
        print(args.key[1:])
        parser.error(f'{args.key} is not a valid key')


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
    parser.add_argument(
        '--key', type=str,
        default='c',
        help="Key. 'es' and 'is' suffixes indicate flat or sharp, respectively. E.g., 'cis' is 'C sharp', while 'ges' is 'G flat'"
    )

    args = parser.parse_args()
    validate_args(parser, args)

    return args
