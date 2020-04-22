import os   
import json
import pandas as pd
import numpy as np
import sys

diri = []
def precalc(diri):
    print("diri before")
    print()

    x_position = 10
    y_position = 10
    gap = 5
    width = 35
    height = 25
    precomputed_position = []
    rect_data = []
    maxwidth = 0
    maxheight = 0
    
    def addToPrecomputedPosition(i, start, level, h, maxwidth, maxheight):
        flag = 0
        if(diri[i]['Args'] == None):
            diri[i]['Args'] = ""
            flag = 1
        val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[i]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
        rect_data.append(val)
        if(flag):
            diri[i]['Args'] = None

        coordinate_a = [width * level + gap, start * height]
        coordinate_b = [(width * level) + width - gap, start * height]
        coordinate_c = [width * level + gap, (start * height) + (height * h) - gap]
        coordinate_d = [(width * level) + width - gap, (start * height) + (height * h) - gap]
        temporary = []
        temporary.append(diri[i]['Line_no'])
        temporary.append(coordinate_a)
        temporary.append(coordinate_b)
        temporary.append(coordinate_c)
        temporary.append(coordinate_d)

        precomputed_position.append(temporary)
        maxwidth = max(maxwidth, coordinate_d[0])
        maxheight = max(maxheight, coordinate_d[1])

        return maxwidth, maxheight

    start = {}
    level = {}
    h = {}

    currentLevel = 0
    close = 0

    for i in range(0, len(diri)):
        bbid = diri[i]['BB_ID']
        method = diri[i]['Method']
        key = bbid+method
        print(key)
        if(diri[i]['Direction'] == ">"):
            currentLevel = currentLevel + 1
            start[key] = i - close
            level[key] = currentLevel
        elif(diri[i]['Direction'] == "<"):
            currentLevel = currentLevel - 1
            close = close + 1
            h[key] = i - start[key] - close + 1
            maxwidth, maxheight = addToPrecomputedPosition(i, start[key], level[key], h[key], maxwidth, maxheight)

    return precomputed_position, rect_data, maxheight, maxwidth