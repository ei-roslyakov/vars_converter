import codecs
import logging
import os
import time
from typing import Generator, Optional, Tuple

import configargparse

import yaml


LOG_FORMAT = "%(asctime)s [%(name)s @ PID:%(process)d " \
             "(%(funcName)s:%(lineno)d)] - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def init_config_parser() -> configargparse.ArgParser:
    parser = configargparse.ArgParser()

    parser.add_argument(
        "--input",
        type=str,
        help="Input file path",
        required=True
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path",
        required=True
    )

    parser.add_argument(
        "--root-key",
        type=str,
        help="Root key in output file",
        required=False,
        default=None
    )

    return parser


def data_extractor(data) -> Generator[Tuple[str, str], None, None]:
    config = data.get("config")
    if not config:
        logger.warning("No 'config' key in config file")
        return

    config_data = config.get("data")
    if not config_data:
        logger.warning("No 'data' key in config file")
        return

    for item in config_data:
        output_item = (item.get("key"), item.get("value"))
        yield output_item


def convert_file(input_file_path: str, output_file_path: str, root_key: Optional[str] = None) -> None:
    logger.info(
        f"Processing file '{input_file_path}' and going to save output "
        f"into '{output_file_path}' with root key '{root_key}''"
    )
    with codecs.open(input_file_path, "r", "utf-8") as input_file:
        file_content = yaml.safe_load(input_file)

    logger.debug(f"YAML file content: {file_content}")

    gathered_data = {}
    for key, value in data_extractor(file_content):
        logger.debug(f"key = '{key}', value = '{value}'")
        gathered_data[key] = value

    if root_key:
        output_data = {
            root_key: gathered_data
        }
    else:
        output_data = gathered_data

    with codecs.open(output_file_path, "w", "utf-8") as output_file:
        yaml.safe_dump(output_data, output_file)


def main() -> int:
    time_start = time.time()
    logger.debug("Application started")
    parser = init_config_parser()
    args = parser.parse_args()
    if not os.path.exists(args.input):
        logger.error(f"Can't find input file {args.input}")
        return -1

    convert_file(
        input_file_path=args.input,
        output_file_path=args.output,
        root_key=args.root_key
    )

    time_end = time.time()
    time_elapsed = round(time_end - time_start, 3)
    logger.debug(f"Application finished. Execution time: {time_elapsed}s")
    return 0


if __name__ == "__main__":
    res = main()
    exit(res)
