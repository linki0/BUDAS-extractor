from shapely.geometry import Polygon, LineString
import numpy as np
from math import pi, sqrt
from graphviz import Graph

def calArea(l):
    x = Polygon([(x[0][0], x[0][1]) for x in l])
    return x.area

# take a single list of number, x[0], y[0], x[1], y[1] ..... as input
def calArea2(l):
    x = Polygon([(l[i], l[i+1]) for i in range(0, len(l), 2)])
    return x.area

def genPoly(l):
    return(Polygon([(x[0][0], x[0][1]) for x in l]))

def genPoly2(l):
    return( Polygon([(l[i], l[i+1]) for i in range(0, len(l), 2)]))

#
#   find the minimum euclidean distance between point 1 and the end point of l2
#   point are in format of [x, y]
#

def euclidean(a, b):
    return sum( [(x-y)**2 for x, y in zip(a, b)])

#
#   find the minimum euclidean distance between a point and the endpoints of a line
#   point are in format of [x, y]
#   line is in format of [ [x1, y2, x2, y2] ]
#
def euclid1(p1, l2):
    return min(euclidean(p1, [l2[0][0], l2[0][1]]), euclidean(p1, [l2[0][2], l2[0][3]]))

#
#  check direction of 3 poitns
#  point are in format of [x, y]
#
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    return np.sign(val)


#
#  assume p, q, r is coliner, check if q is between p and r
#  point are in format of [x, y]
#
def onSegment(p, q, r):
     return (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))

#
#
#  check if two line intersect
#  line is in fromat of [ [x1, y1, x2, y2] ]
#
#
def intersect(l1, l2):
    #print("   check intersect : " + str(l1) + " " + str(l2))
    if (l1[0][0] <= l1[0][2]):
        l1low = [l1[0][0], l1[0][1]]
        l1high = [l1[0][2], l1[0][3]]
    else:
        l1high = [l1[0][0], l1[0][1]]
        l1low = [l1[0][2], l1[0][3]]
    if (l2[0][0] <= l2[0][2]):
        l2low = [l2[0][0], l2[0][1]]
        l2high = [l2[0][2], l2[0][3]]
    else:
        l2high = [l2[0][0], l2[0][1]]
        l2low = [l2[0][2], l2[0][3]]
    o1 = orientation(l1low, l1high, l2low)
    o2 = orientation(l1low, l1high, l2high)
    o3 = orientation(l2low, l2high, l1low)
    o4 = orientation(l2low, l2high, l1high)
    #print("   l1low, l1high, l2low, l2high : " + str(l1low) + " " + str(l1high) + " " + str(l2low) + " " + str(l2high))
    #print("   o1 o2 o3 o4" + str(o1) + " " + str(o2) + " " + str(o3) + " " + str(o4))

    if (o1 != o2) and (o3 != o4):
        return True

    if (o1 == 0  and onSegment(l1low, l2low, l1high)):
        return True

    if (o2 == 0  and onSegment(l1low, l2high, l1high)):
        return True

    if (o3 == 0  and onSegment(l2low,  l1low, l2high)):
        return True

    if (o4 == 0  and onSegment(l2low, l1high, l2high)):
        return True

    return False

#
#  check if line intersect with ANY line on the list 
#  each line is formated [ [x1, y1, x2, y2] ]
#
def checkIntersect(line, linelist):
    res = False
    for l in linelist:
        if (intersect(line, l)):
            res = True
            break
    return res

#
#  check if two lines segment is the same
#  each line is formated [ [x1, y1, x2, y2] ]
#

def equalline(l1, l2):

    if (np.array_equal(l1[0] , l2[0])):
        return True
    else:
        if (np.array_equal(l1[0] , [l2[0][2], l2[0][3], l2[0][0], l2[0][1]])):
           return True
    return False

#
#  return intersection between two line segments 
#  each line is formated [ [x1, y1, x2, y2] ]
#
def line_intersection(line1, line2):
    #print("line intersection : " + str(line1) + " " +str(line2))
    l1 = LineString([(line1[0][0], line1[0][1]), (line1[0][2], line1[0][3])])
    l2 = LineString([(line2[0][0], line2[0][1]), (line2[0][2], line2[0][3])])
    p = l1.intersection(l2)
    #print("   intersected: " + str(p))
    if (p.geom_type == "LineString"):
        plist = list(p.coords)
        return line2[0][0], line2[0][1]

    return int(p.x), int(p.y)


# filp the endpoints of a line
# each line is formated [ [x1, y1, x2, y2] ]
def flipendpt(l):
   return [[l[0][2], l[0][3], l[0][0], l[0][1]]]



#
#  find all the intersection point between a canvas polygon along the horizontal line with y coordinate, 
# 
#  canvas polygon is formated [x1 y1 x2 y2 .... xn yn] (notice that it does NOT go back to x1 y1)
#  return a list of each intersecting segment's x coordinate [ [xlow1, xhigh1] [xlow2, xhigh2] .... ]

def findintersecthori(cpoly, y):
    p = Polygon([(cpoly[i], cpoly[i+1]) for i in range(0, len(cpoly), 2)]) 
    #print("Poly : " + str(p))
    minx = min([cpoly[i] for i in range (0, len(cpoly), 2)])
    maxx = max([cpoly[i] for i in range (0, len(cpoly), 2)])
    l = LineString([(minx, y), (maxx, y)])
    qq = p.intersection(l)
    #print(qq.geom_type)
    if (qq.geom_type == "LineString"):
	    #print(" intersection: " + str(qq))
	    plist = qq.coords
	    #print(" intersection: " + str(plist))
	    #for t in plist:
            #    print("   " + str(t))
	    l1 = [[t[0] for t in plist]]
    elif (qq.geom_type == "MultiLineString"):
        l1 = []
        for qq1 in qq:
            #print(" intersection: " + str(qq1))
            plist = qq1.coords
            #print(" intersection: " + str(plist))
            #for t in plist:
            #     print("   " + str(t))
            l2 = [t[0] for t in plist]
            l1.append(l2)
    #print(" intersection x: " + str(l1))
    return l1
 
	    
#
#  find the intersection line segment between a canvas polygon along the horizontal line that pass through pt = [x y]  ordered
# 
#  canvas polygon is formated [x1 y1 x2 y2 .... xn yn] (notice that it does NOT go back to x1 y1)
#  return a list of each intersecting segment's x coordinate [ x1 y x2 y ] 

def findintersecthoriseg(cpoly, pt):
    l = findintersecthori(cpoly,pt[1])
    res1 = [y for y in l if (y[0] <= pt[0]) and (y[1] >= pt[0])]
    #print(res1)
    return [res1[0][0], pt[1], res1[0][1], pt[1]]
    
   




#
#  find all the intersection point between a canvas polygon along the horizontal line with x coordinate, 
# 
#  canvas polygon is formated [x1 y1 x2 y2 .... xn yn] (notice that it does NOT go back to x1 y1)
#  return a list of each intersecting segment's x coordinate [ [xlow1, xhigh1] [xlow2, xhigh2] .... ]

def findintersectvert(cpoly, x):
    p = Polygon([(cpoly[i], cpoly[i+1]) for i in range(0, len(cpoly), 2)]) 
    #print("Poly : " + str(p))
    miny = min([cpoly[i] for i in range (1, len(cpoly) + 1, 2)])
    maxy = max([cpoly[i] for i in range (1, len(cpoly) + 1, 2)])
    l = LineString([(x, miny), (x, maxy)])
    #print("l : " + str(l))
    qq = p.intersection(l)
    #print(qq.geom_type)
    if (qq.geom_type == "LineString"):
	    #print(" intersection: " + str(qq))
	    plist = qq.coords
	    #print(" intersection: " + str(plist))
	    #for t in plist:
            #    print("   " + str(t))
	    l1 = [[t[1] for t in plist]]
    elif (qq.geom_type == "MultiLineString"):
        l1 = []
        for qq1 in qq:
            #print(" intersection: " + str(qq1))
            plist = qq1.coords
            #print(" intersection: " + str(plist))
            #for t in plist:
            #     print("   " + str(t))
            l2 = [t[1] for t in plist]
            l1.append(l2)
    #print(" intersection x: " + str(l1))
    return l1
 
	    
#
#  find the intersection line segment between a canvas polygon along the horizontal line that pass through pt = [x y]  ordered
# 
#  canvas polygon is formated [x1 y1 x2 y2 .... xn yn] (notice that it does NOT go back to x1 y1)
#  return a list of each intersecting segment's x coordinate [ x1 y x2 y ] 

def findintersectvertseg(cpoly, pt):
    l = findintersectvert(cpoly,pt[0])
    res1 = [y for y in l if (y[0] <= pt[1]) and (y[1] >= pt[1])]
    #print(res1)
    return [pt[0], res1[0][0], pt[0], res1[0][1]]
    
   
#
#   combine  lines that are similar in slope
#   perference given to horizontal and vertical line
#   line in polygon in format [x1 y1 x2 y2 ... xn yn]
def combinelines(p1):
    anglelist = []
    lengthlist = []
    for i in range(0, len(p1)-2, 2):
        if (p1[i] == p1[i+2]):
              anglelist.append(pi/2)
        else:
              anglelist.append(np.arctan((p1[i+3] - p1[i+1]) / (p1[i+2] - p1[i])))
        lengthlist.append(euclidean([p1[i], p1[i+1]], [p1[i+2], p1[i+3]]))
    if (p1[0] == p1[-2]):
          anglelist.append(pi/2)
    else:
          anglelist.append(np.arctan((p1[-1] - p1[1]) / (p1[-2] - p1[0])))
    lengthlist.append(euclidean([p1[0], p1[1]], [p1[-2], p1[-1]]))
    return [anglelist, lengthlist]
          

#
#   check adjacent
#   input list of polygons, door, openings
#   line in polygon in format [x1 y1 x2 y2 ... xn yn]
#   generate a dictionary of edges with value 1 = wall, 2 = door, 3 = opening
#
def checkadjacent(plist, dlist, olist):
    polylist = []
    doorlist = []
    openlist = []
    adjlist = {}
    for x in plist:
        polylist.append(genPoly2(x))
    print(polylist)
    for i in range(0, len(polylist)):
        for j in range(i+1, len(polylist)):
           if (polylist[i].distance(polylist[j]) < 25):
              adjlist[(i, j)] = 1
              print(str(i+1) + " " + str(j+1) + "\n")
    for x in dlist:
        door = LineString([(x[0], x[1]), (x[2], x[3])])
        qq = []
        for i in range(0, len(polylist)):
           if (polylist[i].distance(door) < 25):
              qq.append(i)
        if (len(qq) >= 2):
              for j in range(0, len(qq)):
                 for k in range(j+1, len(qq)):
                    adjlist[(qq[j], qq[k])] = 2
                    print(str(qq[j]+1) + " " + str(qq[k]+1) + "  door\n")
    for x in olist:
        opening = LineString([(x[0], x[1]), (x[2], x[3])])
        qq = []
        for i in range(0, len(polylist)):
           if (polylist[i].distance(opening) < 25):
              qq.append(i)
        if (len(qq) >= 2):
              for j in range(0, len(qq)):
                 for k in range(j+1, len(qq)):
                    adjlist[(qq[j], qq[k])] = 3
                    print(str(qq[j]+1) + " " + str(qq[k]+1) + "  opening\n")
    return adjlist
 
                   
 
                   






