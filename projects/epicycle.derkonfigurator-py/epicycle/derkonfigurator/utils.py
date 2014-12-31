__author__ = 'dima'

import os
import yaml


def read_binary_file(path):
    if not os.path.exists(path):
        return None

    with open(path, 'rb') as f:
        return f.read()


def write_binary_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def read_unicode_file(path):
    data = read_binary_file(path)

    if data is None:
        return data

    return data.decode(encoding='utf-8', errors='strict')


def write_unicode_file(path, data):
    write_binary_file(path, data.encode('utf-8'))


def read_yaml(path):
    data = read_unicode_file(path)

    if data is None:
        return data

    return yaml.load(data)


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)