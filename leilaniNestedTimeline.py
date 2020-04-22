import sys

class Entry:
  def __init__(self,line,lineId):
    self.position = lineId
    tokens = line.strip().split(" ")
    #print(tokens)
    self.callType = tokens[0]
    self.startEnd = "start" if tokens[1] == ">" else "end"
    self.threadId = tokens[2]
    self.name = tokens[3]
    self.bbId = tokens[4]

  def __repr__(self):
    return "("+", ".join(["pos: "+str(self.position),"type: "+self.callType,"start/end: "+self.startEnd,"name: "+self.name,"BB_ID: "+self.bbId])+")"

  def key(self):
    return self.name + "|" + self.bbId

def calculatePositions(testCase):
  complete = {}
  activeMethods = {}
  for i,line in enumerate(testCase):
    obj = Entry(line,i)
    if obj.startEnd == "start": # a new object, add to activeMethods
      activeMethods[obj.key()] = {"y":[i,None],"x":None,"name":obj.name,"BB_ID":obj.bbId,"obj":obj}
    else:
      activeMethods[obj.key()]["y"][1] = i
      activeMethods[obj.key()]["x"] = len(activeMethods) - 1
      complete[obj.key()] = activeMethods[obj.key()]
      del activeMethods[obj.key()]

  # edge case, render starts without ends in order of appearance
  sortedActiveObjects = sorted([activeMethods[k]["obj"] for k in activeMethods],key=lambda obj: obj.position,reverse=True)
  #print(sortedActiveObjects)
  for obj in sortedActiveObjects:
    activeMethods[obj.key()]["y"][1] = len(testCase)
    activeMethods[obj.key()]["x"] = len(activeMethods) - 1
    complete[obj.key()] = activeMethods[obj.key()]
    del activeMethods[obj.key()]

  return complete

if __name__ == "__main__":
  if len(sys.argv) > 1:
    filename = sys.argv[1]
    testCase = []
    with open(filename) as f:
      testCase = f.readlines()
    complete = calculatePositions(testCase)
    for k in complete:
      c = complete[k]
      print("name:",c["name"],"BB_ID:",c["BB_ID"],"y:",c["y"],"x:",c["x"])

