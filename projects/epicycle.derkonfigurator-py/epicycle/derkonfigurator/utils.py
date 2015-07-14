__author__ = 'dima'

import os
import re
import yaml

_DIGITS_RE = re.compile(r"^\d+$")


def read_binary_file(path):
    if not os.path.exists(path):
        return None

    with open(path, 'rb') as f:
        return f.read()


def write_binary_file(path, data, quite=True):
    if quite:
        previous_data = read_binary_file(path)
        if previous_data == data:
            return

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


def join_ipath(*parts):
    return os.path.join(*parts).replace('\\', '/')


def ipath_replace_last_part(path, new_part):
    return join_ipath(os.path.split(path)[0], new_part)


def compare_paths(path1, path2):
    return _normalize_path_for_comparison(path1) == _normalize_path_for_comparison(path2)


def _normalize_path_for_comparison(path):
    return path.replace('\\', '/').lower()


def has_extension(path, extension=None):
    if extension is None:
        return True

    return os.path.splitext(path)[1].lower() == extension.lower()


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def listdir_full(path):
    return [(item, os.path.join(path, item)) for item in os.listdir(path)]


def is_dir_with_file(path, file_name):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, file_name))


def nget(obj, key, default=None):
    if obj is None:
        return default

    return obj[key] if key in obj else default


def split_into_lines(string):
    return string.replace("\r", "").split("\n")


def replace_between(string, new_value, start_token, end_token):
    parts1 = string.split(start_token, 1)

    if len(parts1) == 1:
        return string

    prefix = parts1[0]

    parts2 = parts1[1].split(end_token, 1)

    if len(parts2) == 1:
        return string

    suffix = parts2[1]

    return prefix + start_token + new_value + end_token + suffix


def prefix_lines(data, prefix):
    return "\n".join([prefix + x if x.strip() else x for x in data.split("\n")])


def xml_escape(string):
    return string.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def parse_versioned_name(full_name):
    parts = full_name.split('.')

    name_parts = []
    version_parts = []

    parts.reverse()
    for part in parts:
        if _DIGITS_RE.match(part) and not name_parts:
            version_parts.append(part)
        else:
            name_parts.append(part)

    name_parts.reverse()
    version_parts.reverse()

    name = ".".join(name_parts)
    version = ".".join(version_parts)

    return name, version
