"""
Contains the ReporterLevel class

@author: Dima Potekhin
"""


class ReporterLevel(object):
    def __init__(self, reporter):
        self._reporter = reporter

    def __enter__(self):
        self._reporter.indent()

    def __exit__(self, tipe, value, traceback):
        self._reporter.unindent()
        return False