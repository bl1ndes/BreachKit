#!/usr/bin/env python3

import sys
from breachkit.main import main as scanner_main
from breachkit.menu import main as menu_main

def main():
    """Command-line entry point for BreachKit"""
    if len(sys.argv) > 1:
        # If arguments are provided, run the scanner
        scanner_main()
    else:
        # If no arguments, show the menu
        menu_main()

if __name__ == "__main__":
    main()
