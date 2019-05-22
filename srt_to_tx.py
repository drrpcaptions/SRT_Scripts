#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
'''
Created on May 22, 2019
Updated on May 22, 2019

@author: pablojaku@gmail.com

Python 3.6
'''

# Libraries to import
import sys
import os


# Main program
def main(args):

    # the script will take 2 input , the first is the input file and the second is the output file
    # first file should be a srt file
    if os.path.splitext(os.path.basename(args[1]))[1] != '.srt':
        print("EROOR, input file not SRT")
        exit()

    # second file should be a txt file
    if os.path.splitext(os.path.basename(args[2]))[1] != '.txt':
        print("EROOR, output file not TXT")
        exit()

    # passed input test now assing to variables
    input_file = args[1]
    output_file = args[2]

    with open(input_file) as f:
        lines = f.readlines()
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line)


# Program initiation point
if __name__ == '__main__':
  main(sys.argv)

  
  
  """
    args[1]: input srt subtitles file
    args[2]: output txt file
  """


