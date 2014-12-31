"""
@author: Dima Potekhin
"""

import sys

from epicycle.derkonfigurator import Repository, Reporter


def main():
    """
    The main function of Der Konfigurator
    :rtype : None
    """
    
    if len(sys.argv) != 2:
        print "ERROR: Bad arguments!"
    
    reporter = Reporter()
    
    repository_path = sys.argv[1]
    
    repository = Repository(reporter, repository_path)
    
    repository.configure()
    
main()