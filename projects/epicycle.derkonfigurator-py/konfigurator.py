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
    
    if len(sys.argv) != 3:
        print "ERROR: Bad arguments!"
        sys.exit(-1)

    derkonfigurator_path = sys.argv[1]
    workspace_path = sys.argv[2]

    derkonfigurator = DerKonfigurator(derkonfigurator_path, workspace_path)

    derkonfigurator.run()

main()