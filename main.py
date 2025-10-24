from idml_parser.extract import extract_idml
from idml_parser.spreads import parse_spreads
from idml_parser.stories import parse_stories
from idml_parser.styles import parse_styles
from idml_parser.builder import build_html
from clear_temp import clear_temp
import os
import pathlib as path
import sys
import shutil as shut
import logging as log
import datetime as dt



def main():
    p = path.Path(".")
    log_file = p/"idml_to_html.log"
    if log_file.exists():
        os.remove(log_file)
    log.basicConfig(filename='idml_to_html.log', level=log.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

    temp_folder = p/"temp"
    output_folder = p/'html_output'
    input_file = p / "idml_input" / "signature.idml"
    log.info("Checking output folder")
    if not output_folder.exists():
        log.warning("Output folder does not exist")
        log.info("Creating output folder")
        output_folder.mkdir()
    else:
        log.info("Output folder exists")

    log.info("Checking input file")
    if not input_file.exists():
        log.error("Input file does not exist")
        sys.exit()
    elif input_file.suffix.lower() != '.idml':
        log.error("Input file does not have an IDML file")
        sys.exit()
    else:
        log.info("Input file exists")
    log.info("Checking temporary folder")
    if not temp_folder.exists():
        log.warning("Temporary folder does not exist")
        log.info("Creating temporary folder")
        temp_folder.mkdir()
    else:
        log.info("Temporary folder exists")
    log.info("clearing temp folder")
    clear_temp(temp_folder)

    log.info("Starting extraction of the input file")
    extraction = extract_idml(input_file,temp_folder)
    if extraction:
        log.info("Extraction successful")
    else:
        log.error("Extraction failed")
        log.info("Stopping extraction of the input file")
        sys.exit(1)
    spreads = parse_spreads(temp_folder)
    stories = parse_stories(temp_folder)
    styles = parse_styles(temp_folder)
    build_html(spreads,stories,styles,output_folder)




if __name__ == "__main__":
    main()
