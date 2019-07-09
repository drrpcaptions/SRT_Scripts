# Caption Stats Scripts

./srt_stats     [SRT File (input)] [CSV File (output)]

### Starting Point
Using Dr Kushalnagar 2013 Script to process YouTube Captions as a template, I modified the script to process the same stats for an SRT file.
- the main difference is that instead of feeding YouTube video IDs, you feed the raw SRT file
- second difference is that the old script would process a file with a list of Video IDs (meaning multiple videos processed), while all the new scripts are designed to process one local subtitle file at a time

## Stats
|Value|Formula|Explanation|
|---|---|---|
|wordsPerMin|(numW/totalTime)*60|Words per minute is calculated by taking the number of words, diving it up by the amount of time, and it is multiplied by 60 because the time used inside the code is in seconds|
|wpmMax|max(wpsL)*60|Find the line with the highest words per second, multiply by 60 to change value to minutes|
|totalTime|sum(##lineDurationL)|This value is the total time captions are shown on the screen, NOT the total time of the video. This is calculated and presented in seconds|
|numW|sum(wL)|Absolute number of words|
|numUniqW|len(list(set(lineL)))|Absolute number of unique words|
|pcUniqW|(numUniqW/float(numW))*100|Percentage of unique words|
|aveWL|sum(wL)/float(len(wL))|The average length (characters) of a word in the subtitle file|
|maxWL|max(wL)|Length of longest word in transcript|
|minWL|min(wL)|Length of shortest word in transcript|

## Stats Script - No Checks

the script can be found at [srt_stats_no_checks.py](https://github.com/drrpcaptions/SRT_Scripts/blob/master/srt_stats_no_checks.py)

This is the base script that has no additional programing to 'clean up' the subtitles
In other words, the script assumes that all captions are to be counted as words
- this also accepts a lot of single characters such as - , ♪ , >
- It does count the (),?,!, etc as part of the word length
- Additional descriptors [NSI] are counted as words 
  - ex: (audience, laughs) (Stephen, chuckles)
- Assumes there are no double lines

## Stats Script - REV Subtitles

the script can be found at [srt_rev_stats.py](https://github.com/drrpcaptions/SRT_Scripts/blob/master/srt_rev_stats.py)

This script has some additional programing to ensure the optimal processing for REV generated (curated) SRT Files
- removes the following characters individually:
  - ♪
  - "-"
  - ? (not working at the moment)
  - !
