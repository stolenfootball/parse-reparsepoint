# parse-reparsepoint
Python program to parse out and display reparse point info present in an NTFS MFT entry

## Overview
This project takes a raw NTFS image and an MFT entry number. It then:
- Finds the MFT entry corresponding to the number
- Checks if it belongs to a reparse point
- Analyzes any info it can find in regards to the reparse point

It currently has the ability to resolve the meaning of any reparse tag listed in the Microsoft documentation, and can retrieve information from the reparse data section of the following types of reparse points:
- OneDrive Cloud-only files
- Symbolic Links
- Windows Mount Points

## Installation
This project can be installed with `pip` using the following command:
`python3 -m pip install parse-reparsepoint`

## Usage
```
usage: parse-reparsepoint [-h] -f FILE -m MFT_ENTRY

Parse reparse point

options:
  -h, --help                               show this help message and exit
  -f FILE, --file FILE                     Path to file
  -m MFT_ENTRY, --mft-entry MFT_ENTRY      MFT entry to parse

example:
  parse-reparsepoint -f Windows-10-Dev.raw -m 247645
```
