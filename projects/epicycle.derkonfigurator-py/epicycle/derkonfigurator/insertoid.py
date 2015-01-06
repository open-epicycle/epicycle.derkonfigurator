__author__ = 'Dima Potekhin'

from epicycle.derkonfigurator.utils import replace_between


def has_insertoid(source, name):
    return _get_start(name) in source


def set_insertoid(source, name, value):
    return replace_between(source, value, _get_start(name), _get_end())


def _get_start(name):
    return "[[[[%s>" % name


def _get_end():
    return "]]"+"]]"