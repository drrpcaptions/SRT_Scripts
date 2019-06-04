#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
'''
Created on May 23, 2019
Updated on June 3, 2019

@author: pablojaku@gmail.com

Python 3.6
'''

# Libraries to import
import sys
import os
import pysrt
import difflib


# Support Functions

# Uses sequence matcher
def removeDuplicatedLinesSequence(pre_sub, current_sub):
          # compare with previous text
        repeated_text = difflib.SequenceMatcher(None, pre_sub, current_sub)
        match = max(repeated_text.get_matching_blocks(),
                    key=lambda x: x[2])  # this will be a 3 value object
        i, j, k = match  # get distributed
        match_text = repeated_text.a[i:i+k]  # text is extracted from  object
        # create a create text by deleteing the matching string
        clean_sub = current_sub.replace(match_text, '')
        # strip the new lines
        clean_sub = clean_sub.strip()

        # return the clean sub
        return clean_sub

# Uses assumption that prev will contain A B C D and current will contain B C D E

def removeDuplicatedLinesCompare(pre_sub, current_sub):

    # temp var for camprison to find duplicate
    prev_sub = pre_sub.splitlines()
    this_sub = current_sub.splitlines()
    i = -1

    # how many lines in the sub
    prev_sub_lenght = len(prev_sub)

    # while loop
    while i < prev_sub_lenght:

      # compare prev sub line with current sub line
      # if match
      j = 0
      if prev_sub[i] == this_sub[0]:
        # what ever is still in the prev_sub should be repeated in the current
        repeated_subs = prev_sub[i:]
        # now we follow match
        for sub in repeated_subs:
          if sub == this_sub[j]:
            j += 1
        # now j represents how far into the current subs are already in the previous sub
        clean_sub = ''.join(this_sub[j:])
        print(clean_sub)
        return clean_sub
      # go to the next round
      i += 1

    # if the wile loop completes without a return (exiting the fucntion) then none of the text is copied and the whole current text should be returned
    print('none of the lines match, return whole current sub')
    return(current_sub)

def removeDuplicatedLines(input_file, output_file):

    # open the SRT file into object
    subs=pysrt.open(input_file)

    # temp var for camprison to find duplicate # start with the first and second sub
    prev_sub=subs[0].text
    this_sub=subs[1].text
    first_sub=subs[0].text

    for sub in subs:

        # get the current text
        this_sub=sub.text



        # print(repr(this_sub))

        # clean_sequence_sub = removeDuplicatedLinesSequence(prev_sub,this_sub)


        # print(prev_sub)
        # print(this_sub)
        clean_compare_sub = removeDuplicatedLinesCompare(prev_sub, this_sub)

        # print(clean_sequence_sub)

        # save clean text to srt object
        sub.text = clean_compare_sub

        # prepare the next round
        prev_sub=this_sub

    # all srt objects have been update with clean text
    # except the first on
    subs[0].text=first_sub

    # save to new srt file
    subs.save(output_file, encoding='utf-8')


# Main program
def main(args):

    # the script will take 2 input , the first is the input file and the second is the output file
    # first file should be a srt file
    if os.path.splitext(os.path.basename(args[1]))[1] != '.srt':
        print("EROOR, input file not SRT")
        exit()

    # second file should be a srt file
    if os.path.splitext(os.path.basename(args[2]))[1] != '.srt':
        print("EROOR, output file not SRT")
        exit()

    # passed input test now assing to variables
    input_file=args[1]
    output_file=args[2]

    # Function to remove duplicated lines
    removeDuplicatedLines(input_file, output_file)

    print('Duplicated lines have been elminated at ' + output_file)


# Program initiation point
if __name__ == '__main__':
  main(sys.argv)



  """
    args[1]: input srt subtitles file
    args[2]: output txt file
  """
