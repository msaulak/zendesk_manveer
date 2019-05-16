import glob
import json
import os

def get_file_name_list(pattern, folder):
    list_of_files = glob.glob(os.path.join(folder, pattern))
    if not list_of_files:
        raise FileNotFoundError(f'Files not for pattern {pattern} in folder {folder}')
    return list_of_files


def parse_json_from_file(file_path):
    parsed_json = None
    with open(file_path, 'r') as file_reader:
        parsed_json = json.load(file_reader)
    return parsed_json
