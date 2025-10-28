from idml_parser.extract import extract_idml
from idml_parser.spreads import parse_spreads
from idml_parser.stories import parse_stories
from idml_parser.styles import parse_styles
from idml_parser.builder import build_html
from clear_temp import clear_temp
import os
import pathlib as path
import sys
import logging as log
import argparse


def setup_logging():
    p = path.Path(".")
    log_file = p / "idml_to_html.log"
    if log_file.exists():
        os.remove(log_file)

    log.basicConfig(
        filename=log_file,
        level=log.INFO,
        filemode="w",
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )



def run_conversion():
    p = path.Path(".")
    temp_folder = p / "temp"
    output_folder = p / "html_output"
    input_file = p / "idml_input" / "signature.idml"

    log.info("Checking output folder")
    if not output_folder.exists():
        log.warning("Output folder does not exist — creating it.")
        output_folder.mkdir()

    log.info("Checking input file")
    if not input_file.exists():
        log.error("Input file does not exist.")
        sys.exit(1)
    elif input_file.suffix.lower() != ".idml":
        log.error("Input file is not an IDML file.")
        sys.exit(1)

    log.info("Checking temporary folder")
    if not temp_folder.exists():
        log.warning("Temporary folder does not exist — creating it.")
        temp_folder.mkdir()
    else:
        log.info("Temporary folder exists")

    log.info("Clearing temp folder")
    clear_temp(temp_folder)

    log.info("Starting extraction of the input file")
    if extract_idml(input_file, temp_folder):
        log.info("Extraction successful")
    else:
        log.error("Extraction failed — aborting.")
        sys.exit(1)

    success_spreads, spreads = parse_spreads(temp_folder)
    success_stories, stories = parse_stories(temp_folder)
    success_styles, styles = parse_styles(temp_folder)

    if not (success_spreads and success_stories and success_styles):
        log.error("Parsing failed — aborting.")
        sys.exit(1)

    build_html(spreads, stories, styles, output_folder)
    log.info("HTML build completed successfully.")


def main():
    parser = argparse.ArgumentParser(description="Convert IDML file into HTML signature.")
    parser.add_argument("-ct", "--clear-temp", help="Clear temp folder", action="store_true")
    parser.add_argument("-r", "--run", help="Run full conversion pipeline", action="store_true")
    args = parser.parse_args()

    setup_logging()

    p = path.Path(".")
    temp_folder = p / "temp"

    if args.clear_temp:
        log.info("Clearing temp folder (manual request)")
        clear_temp(temp_folder)

    if args.run:
        run_conversion()
    elif not args.clear_temp:
        parser.print_help()


if __name__ == "__main__":
    main()
