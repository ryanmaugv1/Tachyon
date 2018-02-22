#
#  Tachyon
#  setup.py
#
#  Created on 14/08/17
#  Ryan Maugin <ryan.maugin@adacollege.org.uk>
#

import os
import platform
import sys


class Setup():

    def __init__(self):
        
        print('+------------------------------------------------------+')
        print('|           Installing Tachyon - v1.0.0 alpha          |')
        print('|               Developed By Ryan Maugin               |')
        print('+------------------------------------------------------+')
        print("| Operating System : " + platform.system())
        print("| Release          : " + platform.release())
        print("| Tachyon Version  : v1.0 alpha                     [X]|")


    def setup(self):
        """ Setup

        This method will find the OS install route and then perform the installation
        for that specific OS
        """

        # Check the platform and perform install for that platform
        if platform.system() == "Darwin":

            print('| MacOS Install Route                               [X]|')
            self.mac_osx_install_route()
        elif platform.system() == "Linux":
            print('| Linux install route                               [X]|')
            self.linux_install_route()
        elif platform.system() == "Windows":
            print('| Windows install route                             [X]|')
            self.win_32_install_route()
        else:
            print('| Default install route                             [X]|')
            
        print("+------------------------------------------------------+")


    def mac_osx_install_route(self):
        """ MacOSX Install Route
        
        This method will install the tachyon language on a mac by making a 
        tachyon executable and adding it the /usr/local/bin directory
        """

        # CHOMD +X Changes the permissions of the fle to make it executable
        os.system("chmod +x ./src/main.py")

        print("| Set Tachyon Executable Permission                 [X]|")

        # Add customised directory to the $PATH
        os.system('export PATH="$PATH:$HOME/bin"')
        print("| Add Customised Directory to $PATH                 [X]|")

        # Create a symbolic link to the script
        os.system("ln -s " + os.getcwd() + "/src/main.py /usr/local/bin/tachyon")
        print("| Create Symbolic Link to Script                    [X]|")
        #print(os.getcwd() + "/src/main.py")

    def win_32_install_route(self):
        """ Windows Install Route
        
        This method will install the tachyon language on a windows 
        """
        # Don't think windows needs executable premissions.
        print ("| Set path variable:                                  |")
        print ("| Note: please consult the TROUBLESHOOTING.md for     |")
        print ("| Setting the path variable. You need to do that      |")
        print( "| before you can use tachyon                          |")
        # Create a symbolic link to the script
        self.win_create_bat()
        print("| Create Script to run script                       [X]|")


    def win_create_bat(self):
        # Create file
        file = open("tachyon.bat", "w") # W is for opening in write, and delete if it exists.
        file.write("@echo off\n")
        file.write("py ")
        file.write("\"" + os.getcwd() + "\\src\\main.py\"" + " %~1")
        file.close()


    def linux_install_route(self):
        pass


if __name__ == "__main__":
    # Check dir.
# Check the directory. Maybe do a mv?
    if platform.system() == "Darwin":
        if os.getcwd() != "~/Users/mac/Library/Tachyon":
            ans = raw_input ('You were supposed to clone this into "~/Users/mac/Library" Continue? (y / n)')
            # Exit if answer is not yes. Should do a do..while loop.
            if ans.lower() != 'y':
                sys.exit()
    elif platform.system() == "Linux":
        if os.getcwd() != "~/Tachyon":
            ans = raw_input('You were supposed to clone this into "~/". Continue? (y / n)')
            # Exit if answer is not yes. Should do a do..while loop.
            if ans.lower() != 'y':
                sys.exit()
    elif platform.system() == "Windows":
        pass
    installer = Setup()
    installer.setup()















