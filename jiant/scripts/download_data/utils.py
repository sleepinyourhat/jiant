import nlp
import os
import tarfile
import urllib
import zipfile

import jiant.utils.python.io as py_io


def convert_nlp_dataset_to_examples(path, name=None, version=None,
                                    field_map=None, label_map=None, phase_list=None):
    dataset = nlp.load_dataset(path=path, name=name, version=version)
    if phase_list is None:
        phase_list = dataset.keys()
    examples_dict = {}
    for phase in phase_list:
        phase_examples = []
        for raw_example in dataset[phase]:
            if field_map:
                for old_field_name, new_field_name in field_map.items():
                    raw_example[new_field_name] = raw_example[old_field_name]
                    del raw_example[old_field_name]
            if label_map and "label" in raw_example and raw_example["label"] in label_map:
                raw_example = label_map[raw_example["label"]]
            phase_examples.append(raw_example)
    return examples_dict


def write_examples_to_jsonls(examples_dict, task_data_path):
    os.makedirs(task_data_path, exist_ok=True)
    paths_dict = {}
    for phase, example_list in examples_dict.items():
        jsonl_path = os.path.join(task_data_path, f"{phase}.jsonl")
        py_io.write_jsonl(example_list, jsonl_path)
        paths_dict[phase] = jsonl_path
    return paths_dict



def download_and_unzip(url, extract_location):
    """Downloads and unzips a file, and deletes the zip after"""
    _, file_name = os.path.split(url)
    zip_path = os.path.join(extract_location, file_name)
    download_file(url, zip_path)
    with zipfile.ZipFile(zip_path) as zip_ref:
        zip_ref.extractall(extract_location)
    os.remove(zip_path)


def download_and_untar(url, extract_location):
    _, file_name = os.path.split(url)
    """Downloads and untars a file, and deletes the tar after"""
    tar_path = os.path.join(extract_location, file_name)
    download_file(url, tar_path)
    with tarfile.open(tar_path) as tar:
        tar.extractall(path=extract_location)
    os.remove(tar_path)


def download_file(url, file_path):
    urllib.request.urlretrieve(url, file_path)