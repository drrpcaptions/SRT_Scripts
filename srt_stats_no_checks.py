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
import csv
import re
from datetime import datetime
import pysrt
import difflib


## rewrting old script using pysrt  # https://github.com/byroot/pysrt
def getValues(file_name):

    # open up the srt file
    subs = pysrt.open(file_name)

    # the end process is an array of just the text, extracted for the SRT object
    #print(subs.text)

    # get line durations , in seconds
    lineDurationLPre = [sub.end - sub.start for sub in subs]
    lineDurationL = []
    for time in lineDurationLPre:
        new_time =  (time.minutes * 60) + (time.seconds * 1) + (time.milliseconds/1000)
        #print(new_time)
        lineDurationL.append(new_time)
    #print(len(lineDurationL))

    # build a words array
    words =[]
    for sub in subs:
        words += sub.text.split()

    #print(len(words))
    wL = [len(word) for word in words if len(word) > 3]
    #print(len(wL))
    aveWL = sum(wL)/float(len(wL))

    ## stats
    lineL = words

    maxWL = max(wL)                                      # Length of longest word in transcript
    minWL = min(wL)                                      # min word (shortest)
    #maxLenW = len(max(' '.join(lineL).split(), key=len))    # Length of word with maximum length
    numUniqW = len(list(set(lineL)))                        # Absolute number of unique words
    wpsL = [i/j for i, j in zip(wL, lineDurationL)]      # maximum wps for a single line
    wpmMax = max(wpsL)*60                                   # maximum  wpm for a single lne
    totalTime = sum(lineDurationL)                          # total time for all youtube captions
    numW = sum(wL)                                       # Absolute number of words
    wordsPerMin = (numW/totalTime)*60                       # Derived WPM based on ??
    pcUniqW = (numUniqW/float(numW))*100                    # Percentage of unique words
    nrow = ['%.2f' % wordsPerMin, '%.2f' % wpmMax, '%.2f' % totalTime, numW, numUniqW, '%.2f' % pcUniqW, '%.2f' % aveWL, maxWL, minWL]
    print(nrow)
    return nrow



# Main program
def main(args):

    # the script will take 2 input , the first is the input file and the second is the output file
    # first file should be a srt file
    if os.path.splitext(os.path.basename(args[1]))[1] != '.srt':
        print("EROOR, input file not SRT")
        exit()

    # second file should be a csv file
    if os.path.splitext(os.path.basename(args[2]))[1] != '.csv':
        print("EROOR, output file not CSV")
        exit()

    # passed input test now assing to variables
    input_file = args[1]
    output_file = args[2]

    f = open(output_file, 'w')
    writer = csv.writer(f, delimiter=',')
    header = ["WPM    ", "MaxWPM ", "TotTime (in Seconds)", "WordCt", "UniqW", "pcUniqW", "veLenW", "maxWL", "minWL"]
    print(header)
    writer.writerow(header)
    
    writer.writerow(getValues(input_file))
    print('List processing completed')




# Program initiation point
if __name__ == '__main__':
  main(sys.argv)

  
  
  """
    args[1]: input srt subtitles file
    args[2]: output csv file
  """
"""
## example pysrt obejects
# when you open the srt file you create an object named SubRipFile 
# SubRipFile are list-like objects of SubRipItem instances:
# SubRipItem instances are editable just like pure Python objects:
# example SubRipItem 
 {end': SubRipTime(0, 2, 19, 454),
 'index': 56,
 'position': u'',
 'start': SubRipTime(0, 2, 17, 521),
 'text': u"I'M NOT.\nTHANK YOU SO MUCH."}
# the time format is H M S ms
"""