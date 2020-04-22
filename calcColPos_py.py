
# calculates the column position for a list of events, represented as start and end points.
# assumes we have a list of lists, [[start, end], [start, end], ...]
def computeColumnPositions(startEnds, threadIDForThreadView):
  sortedStartEnds = sorted(list(startEnds),key=lambda t: t[0])
  timeline_data = computeColumnPositionsHelper(sortedStartEnds)
  return getThreadAlso(timeline_data, startEnds, threadIDForThreadView)

def getThreadAlso(timeline_data, startEnds, threadIDForThreadView):
  passingThread = []
  timeline_data[0].append(threadIDForThreadView[0])
  for i in range(1, len(timeline_data)):
    t1 = timeline_data[i][0]
    t2 = timeline_data[i][1]
    j = 1
    while(1):
      if(startEnds[j][0] == t1 and startEnds[j][1] == t2):
        break
      else:
        j += 1
    timeline_data[i].append(threadIDForThreadView[j])
  print("timeline_data after addition: ", timeline_data)
  return computeFinalPositions(timeline_data)

def computeFinalPositions(timeline_data):
  positions = []
  tempData = {}
  width = 25
  gap = 10
  fullHeight = 530
  totalHeight = timeline_data[0][1]

  # Stores all positions in form of [tl, tr, bl, br]
  tempPos = []
  tempPos.append([40, 10])
  tempPos.append([40 + width, 10])
  tempPos.append([40, 530])
  tempPos.append([40 + width, 530])
  tempData["Value"] = tempPos
  tempData["ThreadData"] = 'All'
  positions.append(tempData)
  i = 1
  while(i < len(timeline_data)):
    xPos = 40 + (timeline_data[i][2] * (width + gap))
    tempPos = []
    tempData = {}
    tempPos.append([xPos, remap(timeline_data[i][0], totalHeight)])
    tempPos.append([xPos + width, remap(timeline_data[i][0] + width, totalHeight)])
    tempPos.append([xPos, remap(timeline_data[i][1], totalHeight)])
    tempPos.append([xPos + width, remap(timeline_data[i][1] + width, totalHeight)])
    tempData["Value"] = tempPos
    tempData["ThreadData"] = timeline_data[i][3]
    positions.append(tempData)
    i += 1
  return positions

def remap(x, in_max):
  in_min = 1
  out_min = 10
  out_max = 530
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# calculates the column position for a list of events, represented as start and end points.
# assumes we have a list of lists, [[start, end], [start, end], ...]
# should be sorted by starting value
def computeColumnPositionsHelper(sortedStartEnds):
  pos = {}
  i = 0
  for t in sortedStartEnds:
    s = t[0]
    e = t[1]
    found = False
    for j in sorted(pos):
      ct = pos[j][-1]
      cs = ct[0]
      ce = ct[1]
      if s >= ce:
        pos[j].append(t)
        found = True
        break
    if not found:
      pos[i] = [t]
      i += 1
  res = []
  for j in pos:
    tg = pos[j]
    for t in tg:
      t2 = list(t)
      t2.append(j)
      res.append(t2)
  return res