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

# Support functions

# returns true for ints

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return 

# cleans text when it is being repeated
def noDuplicates(subs):

    # boolen value
    duplicateLines = False

    # temp var for camprison to find duplicate # start with the first and second sub
    prev_sub = subs[0].text
    this_sub = subs[1].text

    # to skip the first iterations
    subs = iter(subs)
    next(subs)
    for sub in subs:

        # get the current text
        this_sub = sub.text

        # compare with previous text
        repeated_text = difflib.SequenceMatcher(None, prev_sub, this_sub)
        match = max(repeated_text.get_matching_blocks(),key=lambda x:x[2]) # this will be a 3 value object
        i,j,k = match # get distributed
        match_text = repeated_text.a[i:i+k] # text is extracted from  object
        #print(match_text)
        if len(match_text.split()) > 3: 
            duplicateLines = True
            print(sub.index)
        # prepare the next round
        prev_sub = this_sub

    # return boolean
    return duplicateLines

# clean text of all remainin weirdities
def deepScrub(subs):

    # finall clean sub arra
    clean_sub_text = []

    # Setting up patterns
    squareBracketsPatter = "\[.*?\]" # removes NSI such [ APPLAUSE ] from text as well
    parenthesisPatter = "\(.*?\)"
    doubleArrowPatter = ">> "

     # washing maching
    for sub in subs:

         # get the current text:
         this_sub = sub.text         

         # Scrubbing
         this_sub = re.sub(squareBracketsPatter, "", this_sub)
         this_sub = re.sub(parenthesisPatter, "", this_sub)
         this_sub = re.sub(doubleArrowPatter, "", this_sub)

         # Deep
         clean_words = this_sub.replace("<i>", "").replace(">>  ", "").replace("</i>", "").replace(">*", "").replace("\n", "").replace("\r", "").replace("\x99","").replace("\xe2","").replace("\xaa","")
    
         # add to the clean text arra
         clean_sub_text += clean_words
    #print(clean_sub_text)

    return clean_sub_text

# 1) get contents + info
# 2) analyze contents of the file
# 3) apped to list and return list of statistics calculated for all files
def getList(fName):
    print(fName)

    # Clean file name
    file_name = os.path.splitext(os.path.basename(fName))[0]

    # load the contents (literally the lines) of the the srt file
    content = open(fName, 'r')

    # Write data file for graphing wpm/wps
    # SRT File will be parsed and the new data file will have the subtitles in a format that is analisis friendly
    f = open('data/'+file_name+'.dat.txt', "w")
    csvW = csv.writer(f, delimiter=',')
    csvW.writerow(["lineStart", "lineDuration", "lineText"])
    # SRT file take 3 or more code line for every singel 'screen' line so the currentLine is the current screen line being processed
    currentLine = 1
    # this is the time stamp pattern used by the SRT files
    tsPattern = "\d\d:\d\d:\d\d,\d\d\d"
    # the srt var becaue each screen line will have the narration over several code lines
    lineText = ""
    # the srt var for the clean words to build a word map for the whole file (this needs to be an array that holds each individual word)
    words = []
    # array to hold all of the line durations for the statics calculation
    lineDurationL = []

    # go throu all the code lines in the file
    for child in content:

        # Remove any time of new lines in the child string
        child = child.replace("\n", "").replace("\r", "")

        # if the line is only a single number then it represents a new sceen line
        if RepresentsInt(child):
            currentLine = currentLine + 1
            print(currentLine)

        # if the line contains a len of 29 characters and 2 tsPattern values then it representes a timespamt for a screen line
        if (len(child) == 29 and len(re.findall(tsPattern, child)) == 2):
            # extract start and end times
            times = re.findall(tsPattern, child)
            startTime = datetime.strptime(times[0], "%H:%M:%S,%f")
            endTime = datetime.strptime(times[1], "%H:%M:%S,%f")
            lineDuration = endTime - startTime
            startTime = startTime.strftime("%H:%M:%S,%f")[:-3]
            #lineDuration = lineDuration.strftime("%H:%M:%S,%f")[:-3]
            lineDuration = lineDuration.total_seconds()
            lineDurationL.append(lineDuration)
            #print (lineDuration)
            #print (len(re.findall(tsPattern,child)))

        # if the line is empty record the compile screen line into the new data file
        if len(child) == 0:
            #print("this line is empty")
            srow = [startTime, lineDuration, lineText]
            csvW.writerow(srow)
            lineText = ""

        # if it is not a number , it is not empty, and does not have 2 tsPattern,       then it is words
        if (RepresentsInt(child) != True and len(child) != 0 and len(re.findall(tsPattern, child)) != 2):
            # raw subtitles
            lineText += child
            # precessed/ cleaned up subtitles
            squareBracketsPatter = "\[.*?\]"
            child = re.sub(squareBracketsPatter, "", child)
            parenthesisPatter = "\(.*?\)"
            child = re.sub(parenthesisPatter, "", child)
            clean_words = child.replace("<i>", "").replace("</i>", "").replace(">*", "").replace(">>", "").replace("\n", "").replace("\r", "").replace("\x99","").replace("\xe2","").replace("\xaa","")
            words += clean_words.split()
            #print("this is words")

        # print(child)
        # print(len(child))

    #print words
    wL = [len(word) for word in words if len(word) > 3]
    print('wl')
    print(wL)
    aveWL = sum(wL)/float(len(wL))
    #print aveWL
    

    # Calculate statistics
    # start = [float(child.get('start') or 0) for child in root]
    print(lineDurationL)
    lineL = []
    lineL = words
    print(lineL)

    
    # list of words' lengths
    wordL = map(lambda x: len(x.split()), lineL)
    print(wordL)
    # Length of longest word in transcript
    maxWL = max(wordL)
    # min word (shortest)
    minWL = min(wordL)
    # maxLenW = len(max(' '.join(lineL).split(), key=len))    # Length of word with maximum length
    # Absolute number of unique words
    numUniqW = len(list(set(lineL)))
    # maximum wps for a single line
    wpsL = [i/j for i, j in zip(wordL, lineDurationL)]
    # maximum  wpm for a single lne
    wpmMax = max(wpsL)*60
    # total time for all youtube captions
    totalTime = sum(lineDurationL)
    # Absolute number of words
    numW = sum(wordL)
    # Derived WPM based on ??
    wordsPerMin = (numW/totalTime)*60
    # Percentage of unique words
    pcUniqW = (numUniqW/float(numW))*100
    nrow = ['%.2f' % wordsPerMin, '%.2f' % wpmMax, '%.2f' % totalTime, numW, numUniqW, '%.2f' % pcUniqW, '%.2f' % aveWL, maxWL, minWL]
    print(nrow)
    return nrow

## rewrting old script using pysrt  # https://github.com/byroot/pysrt
def getValues(file_name):

    # open up the srt file
    subs = pysrt.open(file_name)

    # verify that the data is clean
    if noDuplicates(subs) == True:
        print("ERROR: the file has duplicated lines")
        quit()

    # the end process is an array of just the text, extracted for the SRT object
    print(subs.text)

    # get line durations , in seconds
    lineDurationLPre = [sub.end - sub.start for sub in subs]
    lineDurationL = []
    for time in lineDurationLPre:
        new_time =  (time.minutes * 60) + (time.seconds * 1) + (time.milliseconds/1000)
        print(new_time)
        lineDurationL.append(new_time)
    print(lineDurationL)

    # build a words array
    words =[]
    for sub in subs:
        words += sub.text.split()

    print(words)
    wL = [len(word) for word in words if len(word) > 3]
    print(wL)
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
    header = ["WPM    ", "MaxWPM ", "TotTime", "WordCt", "UniqW", "pcUniqW", "veLenW", "maxWL", "minWL"]
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