# os imports
import os
from os import path as ospath

# pip install regex
import regex as re

# pip install pyyaml
import yaml
import json
import pickle

import codecs
from typing import Union
from LordUtils.json_encoder import JEncoder


# File Path
patternFileName = re.compile(r'[\/\\\?\<\>\|\:\'\"\*,]')  # / \ ? < > | : ' " * ,

# configs
encodes = ["utf-8-sig", "utf-8", "utf-16"]
list_dir_filter = ['.DS_Store', '.git']


def listdir(path, *, only_files=False, only_folders=False, as_fullpath=False):
    l = os.listdir(path)
    for f in list_dir_filter:
        if f in l:
            l.remove(f)
    if only_files:
        l = [f for f in l if ospath.isfile(ospath.join(path, f))]
    if only_folders:
        l = [f for f in l if ospath.isdir(ospath.join(path, f))]
    if as_fullpath:
        l = [ospath.join(path, f) for f in l]
    return l


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def clear_empty_folder(path):
    folders = list(os.walk(path))[1:]
    for folder in folders:
        # folder example: ('FOLDER/3', [], ['file'])
        for i in list_dir_filter:
            if i in folder[0]:
                continue
        if not folder[2] and not folder[1]:
            os.rmdir(folder[0])


def split_extension(f) -> tuple[str, str]:
    """return (file, extension)"""
    return f.rsplit('.', 1) if '.' in f else (f, '')


def split_folder_file(path: str) -> tuple[str, str]:
    """split path to (folder, file)"""
    if os.path.isfile(path):
        folder_path, file_name = path.replace('\\', '/').rsplit('/', maxsplit=1)
        return folder_path, file_name
    else:
        return get_folder_path(path), ''


def get_folder_path(f: str):
    if f.endswith('/') or f.endswith('\\'):
        f = ospath.dirname(f)
    return f


def get_folder_file_name(f: str):
    f = get_folder_path(f)
    f = ospath.basename(f)
    return f


def file_name_check(fileName):
    return patternFileName.sub('', fileName)


def path_check(path):
    """
    Replace illegal characters in file / folder path
    """
    folders = re.split(r"[\\/]", path)
    for i in range(0, len(folders)):
        f = folders[i]
        if i == 0:
            if len(f) == 2 and ":" in f:
                continue
        f = str(file_name_check(f))
        folders[i] = f

    return '/'.join(folders)


def rename_folder(folder_path, new_name) -> str:
    """rename folder to new_name"""
    new_folder_path = ospath.dirname(get_folder_path(folder_path))
    new_name = file_name_check(new_name)
    new_folder_path = ospath.join(new_folder_path, new_name)

    os.rename(folder_path, new_folder_path)
    return new_folder_path


def move_file(file_path, target_path):
    if isinstance(file_path, list):
        for i in file_path:
            move_file(i, target_path)
        return
    if not ospath.isdir(target_path):
        makedirs(target_path)
    file_name = get_folder_file_name(file_path)
    os.rename(file_path, ospath.join(target_path, file_name))


# save load Files

typical_readable_file_endings = {
    'txt',
    'nfo',
    'html',
    'md'
}


def read_file(file: Union[str, list], default=None):
    """
    :param file: file to be loaded. Specification as list to indicate alternative files
    :param default: default return
    """
    _ft = type(file)
    if _ft is str:
        if ospath.exists(file):
            for enc in encodes:
                try:
                    with codecs.open(file, "r", enc) as f:
                        return f.read()
                except:
                    pass
    elif _ft is list:
        for f in file:
            _text = read_file(f)
            if _text:
                return _text
    return default


def typical_readable_file_type(filename):
    _, ending = split_extension(filename)
    return ending in typical_readable_file_endings


# file

def save_file(file, text):
    file = path_check(file)
    dir_path = ospath.dirname(file)
    if not ospath.exists(dir_path):
        makedirs(dir_path)
    with codecs.open(file, "w", encodes[0]) as f:
        f.write(text)
    return True


def open_file(file, mode="w", enc=None):
    if enc is None:
        enc = encodes[0]
    return codecs.open(filename=file, mode=mode, encoding=enc)


# yaml

def load_yaml(y, default=None):
    if os.path.isfile(y):
        y = read_file(y, None)
    if y is None:
        return default

    _yaml = yaml.safe_load(y)
    if isinstance(_yaml, dict):
        return _yaml
    elif isinstance(_yaml, list):
        return _yaml
    else:
        return default


def save_yaml(obj, path):
    _y = yaml.dump(obj)
    return save_file(path, _y)


# json

def load_json(j, default=None):
    if os.path.isfile(j):
        j = read_file(j, None)
    _strip = j.strip()
    if not (_strip.endswith(('}', ']')) and _strip.startswith(('{', '['))):
        return default
    if j is None:
        return default

    _json = json.loads(j)
    return _json


def save_json(obj, path, cls=None):
    if cls is None:
        cls = JEncoder
    _j = json.dumps(obj, indent=2, cls=cls)
    return save_file(path, _j)


# pyobj
# https://www.techcoil.com/blog/how-to-save-and-load-objects-to-and-from-file-in-python-via-facilities-from-the-pickle-module/
# https://www.journaldev.com/15638/python-pickle-example

def save_obj(obj, file):
    file = path_check(file)
    dir_path = ospath.dirname(file)
    if not ospath.exists(dir_path):
        makedirs(dir_path)
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


def load_obj(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
        return data
