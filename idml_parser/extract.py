import os
import pathlib as path
import logging as log

import zipfile

def extract_idml(input_file,temp_folder):
    """
    INPUT : idml file named signature.idml
    :rtype: Unziped idml files (XML files : spreads, stories and styles) stored in the temp folder
    """
    try:
        with zipfile.ZipFile(input_file,'r') as zip_ref:
            zip_ref.extractall(temp_folder)
        return True
    except FileNotFoundError:
        log.error(f"File not found: {input_file}")
        return False

    except zipfile.BadZipFile:
        log.error(f"Invalid IDML file or corrupted archive: {input_file}")
        return False

    except Exception as e:
        log.error(f"Unexpected error during extraction: {e}")
        return False