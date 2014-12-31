"""
Contains the ReporterLevel class

@author: Dima Potekhin
"""


class ReporterLevel(object):
    def __init__(self, reporter):
        self._reporter = reporter

    def __enter__(self):
        self._reporter.ident()

    def __exit__(self, tipe, value, traceback):
        self._reporter.unident()
        return False