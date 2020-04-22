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

    def check_ij(i, j):
        if(diri[i]['Type'] == "API"):
            return True
        elif(diri[i]['Direction'] == ">" and diri[j]['Direction'] == "<" and diri[i]['Method'] == diri[j]['Method']):
        # elif(diri[i]['Direction'] == ">" and diri[j]['Direction'] == "<" and diri[i]['Method'] == diri[j]['Method'] and diri[i]['Args'] == diri[j]['Args']):
            return True
        else:
            return False

    #for 1st i and j not same
    if(not check_ij(i, j)):
        stack.add(i)
        c.add(column)
        positions_stack.add([x_position, y_position])
        all_elements_height.add(0)

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
                flag = 0
                if(diri[stack.peek()]['Args'] == None):
                    diri[stack.peek()]['Args'] = ""
                    flag = 1
                val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
                rect_data.append(val)
                if(flag):
                    diri[stack.peek()]['Args'] = None

                coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
                coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
                coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                temporary = []
                temporary.append(diri[i]['Line_no'])
                temporary.append(coordinate_a)
                temporary.append(coordinate_b)
                temporary.append(coordinate_c)
                temporary.append(coordinate_d)

                precomputed_position.append(temporary)
                maxwidth = max(maxwidth, temporary[1][1])

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

        # if(check_ij(to_check[1], to_check[0]))
        if(check_ij(to_check[1], to_check[0])):
            print("5", i, j)
            stack.pop()
            c.pop()
            positions_stack.pop()
            all_elements_height.pop()

            flag = 0
            if(diri[stack.peek()]['Args'] == None):
                diri[stack.peek()]['Args'] = ""
                flag = 1
            val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
            rect_data.append(val)
            if(flag):
                diri[stack.peek()]['Args'] = None

            coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
            coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
            coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
            coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
            temporary = []
            temporary.append(diri[i]['Line_no'])
            temporary.append(coordinate_a)
            temporary.append(coordinate_b)
            temporary.append(coordinate_c)
            temporary.append(coordinate_d)

            precomputed_position.append(temporary)
            maxwidth = max(maxwidth, temporary[1][1])

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
                flag = 0
                if(diri[stack.peek()]['Args'] == None):
                    diri[stack.peek()]['Args'] = ""
                    flag = 1
                val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
                rect_data.append(val)
                if(flag):
                    diri[stack.peek()]['Args'] = None

                coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
                coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
                coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                temporary = []
                temporary.append(diri[i]['Line_no'])
                temporary.append(coordinate_a)
                temporary.append(coordinate_b)
                temporary.append(coordinate_c)
                temporary.append(coordinate_d)

                precomputed_position.append(temporary)
                maxwidth = max(maxwidth, temporary[1][1])

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

                # New written
                # p = len(a)
                # if(p > 1):
                #     p = p - 1
                for sh in range(len(a) - 1, 0, -1):
                # for sh in range(len(a) - 1, 0, -1):
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
                flag = 0
                if(diri[stack.peek()]['Args'] == None):
                    diri[stack.peek()]['Args'] = ""
                    flag = 1
                val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
                rect_data.append(val)
                if(flag):
                    diri[stack.peek()]['Args'] = None

                coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
                coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
                coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                temporary = []
                temporary.append(diri[i]['Line_no'])
                temporary.append(coordinate_a)
                temporary.append(coordinate_b)
                temporary.append(coordinate_c)
                temporary.append(coordinate_d)

                precomputed_position.append(temporary)
                maxwidth = max(maxwidth, temporary[1][1])

            # if ith element is the same as top element in the stack
            else:
                print("12", i, j)
                stack.pop()
                c.pop()
                positions_stack.pop()
                all_elements_height.pop()

                flag = 0
                if(diri[stack.peek()]['Args'] == None):
                    diri[stack.peek()]['Args'] = ""
                    flag = 1
                val = {"Line_no": diri[i]['Line_no'], "Type": diri[i]['Type'], "Thread_ID": diri[i]['Thread_ID'], "Method": diri[i]['Method'] + '(' + diri[stack.peek()]['Args'] + ')', "Function": diri[i]['Function'], "BB_ID": diri[i]['BB_ID']}
                rect_data.append(val)
                if(flag):
                    diri[stack.peek()]['Args'] = None

                coordinate_a = [positions_stack.peek()[0], positions_stack.peek()[1]]
                coordinate_b = [positions_stack.peek()[0]+40, positions_stack.peek()[1]]
                coordinate_c = [positions_stack.peek()[0], positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                coordinate_d = [positions_stack.peek()[0]+40, positions_stack.peek()[1]+height + (all_elements_height.peek() * (height + in_between_space))]
                temporary = []
                temporary.append(diri[i]['Line_no'])
                temporary.append(coordinate_a)
                temporary.append(coordinate_b)
                temporary.append(coordinate_c)
                temporary.append(coordinate_d)

                precomputed_position.append(temporary)
                maxwidth = max(maxwidth, temporary[1][1])
                
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

    # print(rect_data[:600])

    return precomputed_position, rect_data, maxheight, maxwidth

diri = [{'Line_no': 1, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'},
        {'Line_no': 2, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '>', 'BB_ID': '1073060', 'Method': 'b', 'Args': None, 'Function': '0'},
        {'Line_no': 3, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'b', 'Args': None, 'Function': '0'},
        {'Line_no': 4, 'Type': 'Method', 'Thread_ID': 1, 'Direction': '<', 'BB_ID': '1073060', 'Method': 'a', 'Args': None, 'Function': '0'}]
precomputed_position, rect_data, maxheight, maxwidth = precalc(diri)
print("precomputed_position")
print(precomputed_position)
print("rect_data")
print(rect_data)