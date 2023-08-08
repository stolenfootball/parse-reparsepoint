from inlcude.Navigator import Navigator
from inlcude.Interpreter import Interpreter

import argparse


def main():
    parser = argparse.ArgumentParser(description='Parse reparse point')
    parser.add_argument('-f', '--file', help='Path to file', type=str, required=True)
    parser.add_argument('-m', '--mft-entry', help='MFT entry to parse', type=int, required=True)
    args = parser.parse_args()

    try:
        navigator = Navigator(args.file)
        info = navigator.getEntry(args.mft_entry)
       
        interpreter = Interpreter(info)
        interpreter.printAllInfo()

    except Exception as ex:
        print(ex)
        return

if __name__ == '__main__':
    main()