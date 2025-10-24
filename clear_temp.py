import pathlib as path
import shutil
import shutil as sh
import os

def clear_temp(temp_path:path.Path):
    if temp_path.exists():
        shutil.rmtree(temp_path)
    os.mkdir(temp_path)