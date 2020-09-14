import codecs
import configparser
import logging
import os
import time
from typing import Dict, Generator, Optional, Tuple

import configargparse

import yaml


LOG_FORMAT = "%(asctime)s [%(name)s @ PID:%(process)d " \
             "(%(funcName)s:%(lineno)d)] - %(levelname)s - %(message)s"

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class SupportedOutputFormats(object):
    YAML_FORMAT = "yaml"
    CONFIG_FORMAT = "config"
    KEY_VALUE_AS_TEXT_FORMAT = "kv"


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

    parser.add_argument(
        "--output-format",
        type=str,
        help="Output format",
        required=False,
        default=SupportedOutputFormats.YAML_FORMAT,
        choices=[
            SupportedOutputFormats.YAML_FORMAT,
            SupportedOutputFormats.CONFIG_FORMAT,
            SupportedOutputFormats.KEY_VALUE_AS_TEXT_FORMAT
        ]
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


def save_output_as_yaml(
        data_to_save: Dict,
        output_file_path: str,
        root_key: Optional[str] = None
) -> None:
    if root_key:
        output_data = {
            root_key: data_to_save
        }
    else:
        output_data = data_to_save

    with codecs.open(output_file_path, "w", "utf-8") as output_file:
        yaml.safe_dump(output_data, output_file)


def save_output_as_config(
        data_to_save: Dict,
        output_file_path: str,
        root_key: Optional[str] = None
) -> None:
    if not root_key:
        raise NotImplementedError("To use INI format you need specify root key")

    config = configparser.RawConfigParser()
    config.add_section(root_key)
    for key, value in data_to_save.items():
        config[root_key][key] = value

    with codecs.open(output_file_path, "w", "utf-8") as output_file:
        config.write(output_file)


def save_output_as_raw_key_value_format(
        data_to_save: Dict,
        output_file_path: str
) -> None:
    with codecs.open(output_file_path, "w", "utf-8") as output_file:
        lines_to_save = [f"{key}={value}" for key, value in data_to_save.items()]
        lines_to_save = "\n".join(lines_to_save)
        output_file.writelines(lines_to_save)
        output_file.write("\n")


def convert_file(
        input_file_path: str,
        output_file_path: str,
        output_format: str,
        root_key: Optional[str] = None
) -> None:
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

    if output_format == SupportedOutputFormats.YAML_FORMAT:
        save_output_as_yaml(
            data_to_save=gathered_data,
            output_file_path=output_file_path,
            root_key=root_key
        )
    elif output_format == SupportedOutputFormats.CONFIG_FORMAT:
        save_output_as_config(
            data_to_save=gathered_data,
            output_file_path=output_file_path,
            root_key=root_key
        )
    elif output_format == SupportedOutputFormats.KEY_VALUE_AS_TEXT_FORMAT:
        if root_key:
            logger.warning("Root key will be ignored when saving in raw key-value text format")

        save_output_as_raw_key_value_format(
            data_to_save=gathered_data,
            output_file_path=output_file_path
        )
    else:
        raise NotImplementedError(f"Output format '{output_format}' is not supported")


def main() -> int:
    time_start = time.time()
    logger.debug("Application started")
    parser = init_config_parser()
    args = parser.parse_args()
    if not os.path.exists(args.input):
        logger.error(f"Can't find input file {args.input}")
        return -1

    try:
        convert_file(
            input_file_path=args.input,
            output_file_path=args.output,
            output_format=args.output_format,
            root_key=args.root_key
        )
    except Exception as e:
        logger.error(f"Error converting: {e}")

    time_end = time.time()
    time_elapsed = round(time_end - time_start, 3)
    logger.debug(f"Application finished. Execution time: {time_elapsed}s")
    return 0


if __name__ == "__main__":
    res = main()
    exit(res)
