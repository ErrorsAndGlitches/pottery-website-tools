from argparse import ArgumentParser

from pottery.descriptions import Descriptions


def app_args():
    parser = ArgumentParser(description='Export the descriptions to a CSV')
    parser.add_argument(
        '--output-file',
        required=True,
        help='Output file to write the CSV to.'
    )
    return parser.parse_args()


def main():
    args = app_args()
    Descriptions(args.output_file).run()


if __name__ == '__main__':
    main()
