"""
@author: Dima Potekhin
"""

import sys

from epicycle.derkonfigurator import Reporter
from epicycle.derkonfigurator.workspace import Workspace


def main():
    """
    The main function of Der Konfigurator
    :rtype : None
    """
    
    if len(sys.argv) != 2:
        print "ERROR: Bad arguments!"
    
    reporter = Reporter()
    
    workspace_path = sys.argv[1]
    
    workspace = Workspace(workspace_path, reporter)

    print workspace.path
    
main()