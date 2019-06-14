#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
'''
Created on June 13, 2019
Updated on June 14, 2019

@author: pablojaku@gmail.com

Python 3.6
'''
# Libraries to import
import sys
import os
from difflib import SequenceMatcher

# Support Functions


def alignLines(ref_file, hyp_file):

    # number variables to track stuff
    num_ref_word = 0  # which ref word are we reading now
    num_hyp_word = 0  # which hyp word are we reading now


    # arrays containing lines that will be written into the new files
    ref_curated_lines = []
    hyp_curated_lines = []

    # Read ref file into a word array
    ref_words = []
    with open(ref_file) as f:
        ref_words += [word for line in f for word in line.split()]
    lower_ref_words = [x.lower() for x in ref_words] #lower case array for fair word comparison

    # Read hyp file into a word array
    hyp_words = []
    with open(hyp_file) as f:
        hyp_words += [word for line in f for word in line.split()]
    lower_hyp_words = [x.lower() for x in hyp_words] #lower case array for fair word comparison

    # call the match function

    # now we need to read both files
    # find all the matches
    matches = SequenceMatcher(None, lower_ref_words, lower_hyp_words).get_matching_blocks()
    # populate the curated lines arrays by breaking up the text with matches over 5 words
    for match in matches:
        if(match.size > 5):
            
            #we are going to write everyting between the variables and the current match's location into a new element of the curated array
            ref_curated_lines.append(ref_words[num_ref_word:match.a])
            hyp_curated_lines.append(hyp_words[num_hyp_word:match.b])

            #update varables for next round
            num_ref_word = match.a
            num_hyp_word = match.b

    # write the curated lines to the curated files
    # REF
    with open(str(ref_file)+'.aligned', 'w') as f:
        for line in ref_curated_lines:
            f.write(' '.join(line) + '\n')
    # HYP
    with open(str(hyp_file)+'.aligned', 'w') as f:
        for line in hyp_curated_lines:
            f.write(' '.join(line) + '\n')

# Main program

def main(args):

    # the script will take 2 input , the first is the reference file and the second is the hypothesis file
    # first file should be a txt file
    if os.path.splitext(os.path.basename(args[1]))[1] != '.txt':
        print("ERROR, input file not TXT")
        exit()

    # second file should be a txt file
    if os.path.splitext(os.path.basename(args[2]))[1] != '.txt':
        print("ERROR, output file not TXT")
        exit()

    # passed input test now assing to variables
    ref_file = args[1]
    hyp_file = args[2]

    # Function to  align lines
    alignLines(ref_file, hyp_file)

    print('Aligned files created at ' + ref_file +
          ".aligned  and at " + hyp_file + ".aligned")


# Program initiation point
if __name__ == '__main__':
    main(sys.argv)

    """
    args[1]: input srt subtitles file
    args[2]: output txt file
    ./srt_align_ref_hyp.py Aeneas/Wake\ Up\ Washington/Wake\ Up\ Washington\ Sunday\ -\ Feb\ 24.rev.txt Aeneas/Wake\ Up\ Washington/Wake\ Up\ Washington\ Sunday\ -\ Feb\ 24.txt
  """
