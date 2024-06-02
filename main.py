#!/usr/bin/env python3

#####################################################
# Main Module for "Abacus". A UVSim Virtual Machine #
#                                                   #
# Authors:                                          #
# Kainny Godinez                                    #
# Jackson Jacobson                                  #
# Alex Larsen                                       #
# Scott Mottola                                     #
# Jordan Paxman                                     #
#####################################################

from sys import argv
from uvsim import UVSim

def main():
    """
    Main function. Starts the simulator and executes a program.
    """
    banner()

    if len(argv) != 2:
        print("Please specify a program to execute")
        exit(1)

    
    program = argv[-1]
    uvsim = UVSim()

    uvsim.load(program)
    uvsim.execute()
    

def banner():
    """
    Be fancy. Because why not?
    """
    banner = """
  _    _  __      __   _____   _             
 | |  | | \ \    / /  / ____| (_)            
 | |  | |  \ \  / /  | (___    _   _ __ ___  
 | |  | |   \ \/ /    \___ \  | | | '_ ` _ \ 
 | |__| |    \  /     ____) | | | | | | | | |
  \____/      \/     |_____/  |_| |_| |_| |_|
    """

    print(banner)

if __name__ == '__main__':
    main()
