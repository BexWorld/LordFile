from . import *
from abc import ABC, abstractmethod


class Opener(ABC):
    compatible_endings = []

    @classmethod
    def check(cls, ending):
        return ending in cls.compatible_endings

    @staticmethod
    @abstractmethod
    def load(file):
        pass

    @staticmethod
    @abstractmethod
    def save(obj, file):
        pass


def get_opener(file_ending):
    for cls in Opener.__subclasses__():
        if cls.check(file_ending):
            return cls
    return None


def open_by_type(path, ending=None, default=None):
    if ending is None:
        _, ending = split_extension(path)
    opener_cls = get_opener(ending)
    if opener_cls is None:
        return default
    return opener_cls.load(path)


def save_by_type(obj, path, ending=None, default=None):
    if ending is None:
        _, ending = split_extension(path)
    opener_cls = get_opener(ending)
    if opener_cls is None:
        return default
    return opener_cls.save(obj, path)


class JsonOpener(Opener):
    compatible_endings = ['json']

    @staticmethod
    def load(file, default=None) -> dict:
        return load_json(file, default=None)

    @staticmethod
    def save(obj, file):
        return save_json(obj, file)


class YamlOpener(Opener):
    compatible_endings = ['yaml', 'yml']

    @staticmethod
    def load(file, default=None) -> dict:
        return load_yaml(file, default=None)

    @staticmethod
    def save(obj, file):
        return save_yaml(obj, file)


class PickleOpener(Opener):
    compatible_endings = ['pickle']

    @staticmethod
    def load(file, default=None) -> dict:
        return load_obj(file)

    @staticmethod
    def save(obj, file):
        return save_obj(obj, file)


class TextOpener(Opener):
    compatible_endings = ['txt']

    @staticmethod
    def load(file, default=None):
        return read_file(file, default=None)

    @staticmethod
    def save(text, file):
        return save_file(file, text)