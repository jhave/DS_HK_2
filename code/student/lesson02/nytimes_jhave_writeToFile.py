#!/usr/bin/python
# Import required libraries
from __future__ import division
import sys


""" Updated:
The average age in the file
Click through rate (avg clicks per impression)
The oldest person in the file"""


"""

# HEADERS:

"age", "gender", "signed_in", "avg_click", "avg_impressions", "max_click", "max_impressions"

"""

# Start a counter and store the textfile in memory
total_age = 0
current_age=0
impressions = 0
clicks = 0
oldest_person = 0

lines = sys.stdin.readlines()
lines.pop(0)
n = len(lines)

# For each line
for line in lines:

  clean_line = line.strip().split(',')
  total_age = total_age + int(clean_line[0])
  current_age = int(clean_line[0])

  impressions = impressions + int(clean_line[2])
  clicks = clicks + int(clean_line[3])

  # check to see if my recent age is oldest 
  if current_age > int(oldest_person):
      oldest_person=current_age


print 'Total Unique Visitors: ', n
print 'Total Impressions: ', impressions
print 'Average Age: ', round(total_age/n,2)
print 'Average Clicks per Impressions: ', clicks/impressions
print 'Oldest Person: ', oldest_person


# print HEADERS to file using https://docs.python.org/2/library/fileinput.html#module-fileinput
#
# Open a file
fo = open("foo.txt", "wb")
print "Name of the file: ", fo.name

import fileinput

headers = 'age, gender signed_in avg_click, avg_impressions max_click max_impressions'.split()
for line in fileinput.input(['thefile.blah'], inplace=True):
    if fileinput.isfirstline():
        print '\t'.join(headers)
    print line

# Close opend file
fo.close()