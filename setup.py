#
#  Tachyon
#  setup.py
#
#  Created on 14/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os
import platform

class Setup():

    def __init__(self):
        
        print('+------------------------------------------------------+')
        print('|           Installing Tachyon - v1.0.0 alpha          |')
        print('|               Developed By Ryan Maugin               |')
        print('+------------------------------------------------------+')
        print("| Operating System : " + platform.system())
        print("| Release          : " + platform.release())
        print("| Tachyon Version  : v1.0 alpha                     []|")


    def setup(self):
        """ Setup

        This method will find the OS install route and then perform the installation
        for that specific OS
        """

        # Check the platform and perform install for that platform
        if platform.system() == "Darwin":
            print('| MacOS Install Route                               []|')
            self.mac_osx_install_route()
        elif platform.system() == "Linux":
            print('| Linux install route                               []|')
        elif platform.system() == "Windows":
            print('| Windows install route                             []|')
        else:
            print('| Default install route                             []|')
            
        print("+------------------------------------------------------+")


    def mac_osx_install_route(self):
        """ MacOSX Install Route
        
        This method will install the tachyon language on a mac by making a 
        tachyon executable and adding it the /usr/local/bin directory
        """

        # CHOMD +X Changes the permissions of the fle to make it executable
        os.system("chmod +x ./src/main.py")
        print("| Set Tachyon Executable Permission                 []|")

        # Add customised directory to the $PATH
        os.system('export PATH="$PATH:$HOME/bin"')
        print("| Add Customised Directory to $PATH                 []|")

        # Create a symbolic link to the script
        os.system("ln -s " + os.getcwd() + "/src/main.py /usr/local/bin/tachyon")
        print("| Create Symbolic Link to Script                    []|")
        #print(os.getcwd() + "/src/main.py")


if __name__ == "__main__":
    installer = Setup()
    installer.setup()















