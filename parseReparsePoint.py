import argparse

def main():
    parser = argparse.ArgumentParser(description='Parse reparse point')
    parser.add_argument('-f', '--file', help='Path to file')
    parser.add_argument('-m', '--mft-entry', help='MFT entry to parse')
    args = parser.parse_args()