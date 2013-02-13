#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from http://www.fec.gov/disclosurep/PDownload.do"""

import fileinput
import csv

## Data read
candidates = set()
cMap = {}
cMap['aggregate'] = {'contribs':[]}

for row in csv.reader(fileinput.input()):
    if not fileinput.isfirstline():
        candidate = row[2]
        contrib = float(row[9])
        candidates.add(candidate)
        if (candidate not in cMap):
            cMap[candidate] = {'contribs':[]}
        cMap[candidate]['contribs'].append(contrib)
        cMap['aggregate']['contribs'].append(contrib)

numContributions = len(cMap['aggregate']['contribs'])

if (numContributions == 0):
    print "No data received! Exiting..."
    import sys
    sys.exit(-1)

## Function definitions

def getAverage(array):
    return sum(array)/float(len(array))

def getStandardDev(array):
    mean = getAverage(array)
    return getAverage([(val - mean)**2 for val in array])**0.5

def getMedian(array):
    from math import floor
    array = sorted(array)
    midx = int(floor(len(array) / 2))
    median = array[midx]
    if (len(array) % 2 == 0):
        median = (array[midx] + array[midx - 1])/ 2.0
    return median

def minmax_normalize(value, maximum, minimum):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    newMin = 0
    newMax = 1
    norm = ((value - minimum) / (maximum - minimum)) * (newMax - newMin) + newMin
    return norm

def zscore(value, mean, sd):
    return (value - mean) / sd

def printStats(stats, name):
    total = stats['total']
    minimum = stats['minimum']
    maximum = stats['maximum']
    mean = stats['mean']
    median = stats['median']
    sd = stats['sd']

    print "\n" + "#"*20+"\nStats for: " + name +"\n"+"#"*20

    ##### Print out the stats
    print "Total: %s" % total
    print "Minimum: %s" % minimum
    print "Maximum: %s" % maximum
    print "Mean: %s" % mean
    print "Median: %s" % median
    # square root can be calculated with N**0.5
    print "Standard Deviation: %s" % sd

    ##### Normalize some sample values
    values = [2500, 50, 250, 35, 8, 100, 19]
    print "Values before: %r" % values
    print "Min-max normalized values: %r" % map(lambda val: minmax_normalize(val, maximum, minimum), values)
    print "Z-score values: %r" % map(lambda val: zscore(val, mean, sd), values)

##### Comma separated list of unique candidate names
print "Candidates: " + ', '.join(candidates)

keys = cMap.keys()
keys.remove('aggregate')

for key in ['aggregate'] + keys:
    stats = cMap[key]
    contributions = stats['contribs']
    ## Set variables
    stats['total'] = sum(contributions)
    stats['minimum'] = min(contributions)
    stats['maximum'] = max(contributions)
    stats['mean'] = getAverage(contributions)
    stats['median'] = getMedian(contributions)
    stats['sd'] = getStandardDev(contributions)
    printStats(stats, key)



