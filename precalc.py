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

    # returns stack in form of array in LIFO manner
    def toArray(self):
        return self.stack[::-1]

    # returns stack in form of list
    def toNormalArray(self):
        return self.stack

    # clears the stack and returns empty stack
    def clear(self):
        self.stack = []
        return self.stack

def precalc(diri):
    # diri = [{'Line_no': 1, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'}, {'Line_no': 2, 'Type': 'API', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '56789', 'Method': 'b', 'Args': None, 'Function': '0'}, {'Line_no': 3, 'Type': 'API', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '56789', 'Method': 'b', 'Args': None, 'Function': '0'}, {'Line_no': 4, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 5, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 6, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'd', 'Args': None, 'Function': '0'}, {'Line_no': 7, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'c', 'Args': None, 'Function': '0'}, {'Line_no': 8, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'}, {'Line_no': 9, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'f', 'Args': None, 'Function': '0'}, {'Line_no': 10, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'g', 'Args': None, 'Function': '0'}, {'Line_no': 11, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'h', 'Args': None, 'Function': '0'}, {'Line_no': 12, 'Type': 'API', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '45678', 'Method': 'i', 'Args': None, 'Function': '0'}, {'Line_no': 13, 'Type': 'API', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '45678', 'Method': 'i', 'Args': None, 'Function': '0'}, {'Line_no': 14, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'h', 'Args': None, 'Function': '0'}, {'Line_no': 15, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'g', 'Args': None, 'Function': '0'}, {'Line_no': 16, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'f', 'Args': None, 'Function': '0'}]
    stack = Stack()
    all_elements_height = Stack()
    positions_stack = Stack()
    c = Stack()

    i = 0
    j = 1

    x_position = 10
    y_position = 10
    in_between_space = 5
    width = 40
    height = 25
    column = 0

    maxheight = 0
    maxwidth = 0

    precomputed_position = []
    rect_data = []

    def addToPrecomputedPosition(diri, topStackIndex, i, topAllElementsHeight, maxwidth):
        flag = 0
        if(diri[topStackIndex]['Args'] == None):
            diri[topStackIndex]['Args'] = ""
            flag = 1
        val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[topStackIndex]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
        rect_data.append(val)
        if(flag):
            diri[topStackIndex]['Args'] = None

        coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
        coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
        coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (topAllElementsHeight * (height + in_between_space))]
        coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (topAllElementsHeight * (height + in_between_space))]
        temporary = []
        temporary.append(diri[i]['Line_no'])
        temporary.append(coordinate_a)
        temporary.append(coordinate_b)
        temporary.append(coordinate_c)
        temporary.append(coordinate_d)

        precomputed_position.append(temporary)
        maxwidth = max(maxwidth, temporary[1][1])

    def check_ij(i, j):
        print(i)
        print(j)
        print("end")
        if(diri[i]['Direction'] == ">" and diri[j]['Direction'] == "<" and diri[i]['Method'] == diri[j]['Method']):
            return True
        else:
            return False

    # #for 1st i and j same
    # if(check_ij(i, j)):
    #     print("-1")
    #     flag = 0
    #     if(diri[0]['Args'] == None):
    #         diri[0]['Args'] = ""
    #         flag = 1
    #     val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[i]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
    #     rect_data.append(val)
    #     if(flag):
    #         diri[0]['Args'] = None

    #     coordinate_a = [10,10]
    #     coordinate_b = [10 + 40, 10]
    #     coordinate_c = [10, 10+height + (0 * (height + in_between_space))]
    #     coordinate_d = [10+40, 10+height + (0 * (height + in_between_space))]
    #     temporary = []
    #     temporary.append(diri[i]['Line_no'])
    #     temporary.append(coordinate_a)
    #     temporary.append(coordinate_b)
    #     temporary.append(coordinate_c)
    #     temporary.append(coordinate_d)

    #     precomputed_position.append(temporary)
    #     maxwidth = max(maxwidth, temporary[1][1])

    #     y_position = y_position + height + in_between_space

    #     i = i + 2
    #     j = j + 2

    #for 1st i and j not same
    if(not check_ij(i, j)):
        stack.add(i)
        c.add(column)
        positions_stack.add([x_position, y_position])
        all_elements_height.add(0)

        # Setting (x,y) position and column for next loop
        x_position = x_position + width + in_between_space
        y_position = y_position + height + in_between_space

        column = column + 1
        i = i + 1
        j = j + 1

    #until i is last element and j is no element or i is second last element and j is last element
    while(i < len(diri) and j < len(diri)):
        if(stack.peek() == i or stack.peek() == -1):
            print("1", i, j)
            print(stack.peek())
            if(stack.peek() != -1):
                print("2", i, j)
                addToPrecomputedPosition(diri, stack.peek(), i, all_elements_height.peek(), maxwidth)
                x_position = x_position - (width + in_between_space)
                column = column - 1
                i = i + 2
                j = j + 2
                stack.pop()
                c.pop()
                positions_stack.pop()
                all_elements_height.pop()
        print("3", i, j)
        stack.add(i)
        c.add(column)
        positions_stack.add([x_position, y_position])
        all_elements_height.add(0)

        # checking i with the top of the stack
        # if ith element is same as the top of the element
        to_check = stack.toArray()
        print("to_check", to_check)

        if(len(to_check) == 1):
            print("4", i, j)
            x_position = x_position + width + in_between_space
            y_position = y_position + height + in_between_space

            column = column + 1

            stack.add(j)
            c.add(column)
            positions_stack.add([x_position, y_position])
            all_elements_height.add(0)

            to_check = stack.toArray()
            print("to_check", to_check)

        # if(check_ij(to_check[1], to_check[0]))
        if(check_ij(to_check[1], to_check[0])):
            print("5", i, j)
            stack.pop()
            c.pop()
            positions_stack.pop()
            all_elements_height.pop()

            addToPrecomputedPosition(diri, stack.peek(), i, all_elements_height.peek(), maxwidth)

            if(c.peek() < column):
                column = column - 1
                x_position = x_position - (width + in_between_space)

            stack.pop()
            c.pop()
            positions_stack.pop()
            all_elements_height.pop()

            i = i + 1
            j = j + 1

        # if ith element is not the same as the top of the stack
        else:
            print("6", i, j)
            # check with jth element
            # if it is the same as the jth element
            if(check_ij(i, j)):
                print("7", i, j)
                addToPrecomputedPosition(diri, stack.peek(), i, all_elements_height.peek(), maxwidth)

                stack.pop()
                c.pop()
                positions_stack.pop()
                all_elements_height.pop()

                a = all_elements_height.toArray()
                all_elements_height.clear()
                for sh in range(len(a) - 1, -1, -1):
                    a[sh] = a[sh] + 1
                    all_elements_height.add(a[sh])

                if(c.peek() >= column and c.peek() != 0):
                    column = column - 1
                    x_position = x_position - (width + in_between_space)

                y_position = y_position + height + (in_between_space)
                i = i + 2
                j = j + 2

            # if it is not same as the jth element
            else:
                print("8", i, j)
                a = all_elements_height.toArray()
                all_elements_height.clear()

                for sh in range(len(a) - 1, 0, -1):
                    a[sh] = a[sh] + 1
                    all_elements_height.add(a[sh])
                all_elements_height.add(a[0])

                y_position = y_position + height + in_between_space
                x_position = x_position + width + in_between_space

                column = column + 1
                i = i + 1
                j = j + 1


    # Point where i is last element and j is out of that diri array
    if((i == (len(diri) - 1) and j >= len(diri))):
        print("9", i, j)
        y_position = y_position + (4 * in_between_space)

        stack.add(i)
        c.add(column)
        positions_stack.add([x_position, y_position])
        all_elements_height.add(0)

        # if ith element is not the same as the top of the element
        if(not check_ij(stack.peek(), i)):
            print("10", i, j)
            if(len(stack.toArray()) == 1):
                print("11", i, j)
                addToPrecomputedPosition(diri, stack.peek(), i, all_elements_height.peek(), maxwidth)

            # if ith element is the same as top element in the stack
            else:
                print("12", i, j)
                stack.pop()
                c.pop()
                positions_stack.pop()
                all_elements_height.pop()

                addToPrecomputedPosition(diri, stack.peek(), i, all_elements_height.peek(), maxwidth)
                
                stack.pop()
                c.pop()
                positions_stack.pop()
                all_elements_height.pop()

    while(stack.size()!=0):
        print("13", i, j)
        if(stack.peek() != -1):
            print("14", i, j)
            flag = 0
            if(diri[stack.peek()]['Args'] == None):
                diri[stack.peek()]['Args'] = ""
                flag = 1
            val = {"Line_no": diri[stack.peek()]['Line_no'], "Type": diri[stack.peek()]['Type'], "Thread_ID": diri[stack.peek()]['Thread_ID'], "Method": diri[stack.peek()]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[stack.peek()]['Function'], "BB_ID": diri[stack.peek()]['BB_ID']}
            rect_data.append(val)
            if(flag):
                diri[stack.peek()]['Args'] = None

            coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
            coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
            coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
            coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
            temporary = []
            temporary.append(diri[stack.peek()]['Line_no'])
            temporary.append(coordinate_a)
            temporary.append(coordinate_b)
            temporary.append(coordinate_c)
            temporary.append(coordinate_d)

            maxheight = max(maxheight, coordinate_d[1])

            precomputed_position.append(temporary)
            maxwidth = max(maxwidth, temporary[1][1])

        stack.pop()
        c.pop()
        positions_stack.pop()
        all_elements_height.pop()
    return precomputed_position, rect_data, maxheight, maxwidth