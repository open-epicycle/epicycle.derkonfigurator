"""
Contains the RepositoryPart class

@author: Dima Potekhin
"""

import os
import yaml


class RepositoryPart(object):
    """
    This class represents an object that is part of the repository and has its data in a specific directory
    """

    def __init__(self, reporter, absolute_path):
        """
        Constructor
        """
        
        self._reporter = reporter
        self._path = absolute_path
        
    def get_path(self):
        return self._path
        
    def to_absolute_path(self, *sub_path_parts):
        return os.path.join(self._path, *sub_path_parts)
    
    def get_reporter(self):
        return self._reporter
    
    def report(self, text):
        self._reporter.report(text)
    
    def report_sub_level(self):
        return self._reporter.sub_level()
    
    def read_binary_file(self, sub_path):
        if not os.path.exists(self.to_absolute_path(sub_path)):
            return None
        
        with open(self.to_absolute_path(sub_path), 'rb') as f:
            return f.read()
        
    def write_binary_file(self, sub_path, data):
        with open(self.to_absolute_path(sub_path), 'wb') as f:
            f.write(data)
            
    def read_unicode_file(self, sub_path):
        data = self.read_binary_file(sub_path)
        
        if data is None:
            return data
        
        return data.decode(encoding='utf-8', errors='strict')
        
    def write_unicode_file(self, sub_path, data):
        self.write_binary_file(sub_path, data.encode('utf-8'))
        
    def read_yaml(self, sub_path):
        data = self.read_unicode_file(sub_path)
        
        if data is None:
            return data
        
        return yaml.load(data) 
    
    def ensure_dir(self, *sub_path_parts):
        fir_path = self.to_absolute_path(*sub_path_parts)
        
        if not os.path.exists(fir_path):
            os.makedirs(fir_path)