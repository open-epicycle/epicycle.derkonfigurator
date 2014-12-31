"""
@author: Dima Potekhin
"""

import sys

from epicycle.derkonfigurator import DerKonfigurator


def main():
    """
    The main function of Der Konfigurator
    :rtype : None
    """
    
    if len(sys.argv) != 2:
        print "ERROR: Bad arguments!"
    
    workspace_path = sys.argv[1]

    derkonfigurator = DerKonfigurator(workspace_path)

    derkonfigurator.run()

main()