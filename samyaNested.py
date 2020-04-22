import os   
import json
import pandas as pd
import numpy as np
import sys

class Stack:
    def __init__(self):
        self.stack = []

    def add(self, dataval):
    # Use list append method to add element
        self.stack.append(dataval)

    # Use peek to look at the top of the stack
    def peek(self):     
        if(len(self.stack) == 0):
            return -1
        return self.stack[-1]

    # Use list pop method to remove element
    def pop(self):
        if(len(self.stack) == 0):
            return self.stack
        return self.stack.pop()

    # Use to give the size of the stack
    def size(self):
        return len(self.stack)

def precalc(diri):
    # diri = [{'Line_no': 1, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'}, {'Line_no': 2, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 3, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 4, 'Type': 'API', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '45678', 'Method': 'p', 'Args': None, 'Function': '0'}, {'Line_no': 5, 'Type': 'API', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '45678', 'Method': 'p', 'Args': None, 'Function': '0'}, {'Line_no': 6, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 7, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 8, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'}]
    x_position = 10
    y_position = 10
    gap = 5
    width = 40
    height = 25

    maxheight = 0
    maxwidth = 0
    maxstacksize = -1
    prevx = -1
    prevy = -1
    prevxbase = -1
    prevybase = -1

    precomputed_position = []
    rect_data = []

    def draw(column, effectivePopped, i, maxwidth, maxheight, y_position, prevx, prevy):
        flag = 0
        if(diri[i]['Args'] == None):
            diri[i]['Args'] = ""
            flag = 1
        val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[i]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
        rect_data.append(val)
        if(flag):
            diri[i]['Args'] = None

        coordinate_a = []
        coordinate_b = []
        coordinate_c = []
        coordinate_d = []
        effectiveColumn = column - 1
        if(stack.peek()[1] == 1):
            print("1")
            if(prevx != -1 and prevy != -1):
                print("2")
                x = x_position + (effectiveColumn * (width + gap))
                y = y_position + (effectiveColumn * height) + gap

                coordinate_a = [x, y]
                coordinate_b = [x + width, y]
                coordinate_c = [x, prevy]
                coordinate_d = [x + width, y + prevy]
                prevx = x
            else:
                print("3")
                x = x_position + (effectiveColumn * (width + gap))
                y = y_position + (effectiveColumn * height) + gap

                coordinate_a = [x, y]
                coordinate_b = [x + width, y]
                coordinate_c = [x, y + 25]
                coordinate_d = [x + width, y + 25]
                prevx = x
                prevy = y + 25
        else:
            print("4")
            x = x_position + (effectiveColumn * (width + gap))
            y = prevy + gap

            coordinate_a = [x, y]
            coordinate_b = [x + width, y]
            coordinate_c = [x, y + 25]
            coordinate_d = [x + width, y + 25]

            prevx = x
            prevy = y + 25

        temporary = []
        temporary.append(diri[i]['Line_no'])
        temporary.append(coordinate_a)
        temporary.append(coordinate_b)
        temporary.append(coordinate_c)
        temporary.append(coordinate_d)

        precomputed_position.append(temporary)
        maxwidth = max(maxwidth, coordinate_d[0])
        maxheight = max(maxheight, coordinate_d[1])

        return maxwidth, maxheight, prevx, prevy

    # Main Function
    stack = Stack()
    effectivePopped = 0
    i = 0
    flag = 1
    levely = {}
    lvar = 0

    while(i < len(diri)):
        if(diri[i]['Direction'] == '>'):
            lvar = lvar + 1
            levely[lvar] = prevy
            print("Stack")
            print(stack.size())
            print(maxstacksize)
            if(stack.size() > maxstacksize):
                maxstacksize = maxstacksize + 1
                stack.add([i, 1])
            else:
                stack.add([i, 0])
                if(flag == 1):
                    prevy = prevy + 25
            flag = 1
        else:
            print("#")
            maxwidth, maxheight, prevx, prevy = draw(stack.size(), effectivePopped + 1, stack.peek()[0], maxwidth, maxheight, y_position, prevx, prevy)
            stack.pop()
            effectivePopped = effectivePopped + 1
            flag = 0
        i = i + 1
        print("i")
        print(i)
        print(prevx, prevy)

    return precomputed_position, rect_data, maxheight, maxwidth

# diri = [{'Line_no': 1, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '3456788', 'Method': 'a', 'Args': None, 'Function': '0'}, {'Line_no': 2, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'b', 'Args': None, 'Function': '0'}, {'Line_no': 3, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 4, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 5, 'Type': 'API', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '45678', 'Method': 'e', 'Args': None, 'Function': '0'}, {'Line_no': 6, 'Type': 'API', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '45678', 'Method': 'e', 'Args': None, 'Function': '0'}, {'Line_no': 7, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 8, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 9, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'b', 'Args': None, 'Function': '0'}, {'Line_no': 10, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'p', 'Args': None, 'Function': '0'}, {'Line_no': 11, 'Type': 'API', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '45678', 'Method': 'q', 'Args': None, 'Function': '0'}, {'Line_no': 12, 'Type': 'API', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '45678', 'Method': 'q', 'Args': None, 'Function': '0'}, {'Line_no': 13, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'p', 'Args': None, 'Function': '0'}]
# precomputed_position, rect_data, maxheight, maxwidth = precalc(diri)
# print(precomputed_position)
# print(rect_data)