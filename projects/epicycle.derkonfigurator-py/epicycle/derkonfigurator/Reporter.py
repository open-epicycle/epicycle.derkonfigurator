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
        
        self._identation_level = 0
        
    def ident(self):
        self._identation_level += 1
        
    def unident(self):
        self._identation_level -= 1
        
    def sub_level(self):
        return ReporterLevel(self)
        
    def report(self, text):
        line = ""
        line += "  " * self._identation_level
        line += "- "        
        line += text
        print line
