#
#  Tachyon
#  setup.py
#
#  Created on 14/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import platform

class Setup():

    def __init__(self):
        
        print('--------------------------------------------------------')
        print('|           Installing Tachyon - v1.0.0 alpha          |')
        print('|               Developed By Ryan Maugin               |')
        print('--------------------------------------------------------')
        print("- Operating System : " + platform.system())
        print("- Release          : " + platform.release())
        print("- Tachyon Version  : v1.0 alpha")

    def setup(self):
        
        if platform.system() == "Darwin":
            print('- MacOS install route')
        elif platform.system() == "Linux":
            print('- Linux install route')
        elif platform.system() == "Windows":
            print('- Windows install route')
        else:
            print('- Default install route')

        print("--------------------------------------------------------")

if __name__ == "__main__":
    installer = Setup()
    installer.setup()