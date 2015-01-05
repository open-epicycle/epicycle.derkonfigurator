"""
Contains the Reporter class 

@author: Dima Potekhin
"""

from ReporterLevel import ReporterLevel


class Reporter(object):
    """
    This class reports things to the monitor
    """

    def __init__(self):
        """
        Constructor
        """
        
        self._indentation_level = 0
        
    def indent(self):
        self._indentation_level += 1
        
    def unindent(self):
        self._indentation_level -= 1
        
    def sub_level(self):
        return ReporterLevel(self)
        
    def report(self, text):
        line = ""
        line += "  " * self._indentation_level
        line += "- "        
        line += text
        print line
