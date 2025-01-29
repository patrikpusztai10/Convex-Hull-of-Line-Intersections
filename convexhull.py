import numpy as nmp
import turtle
from horology import timed
from memory_profiler import profile
class ConvexHull:
    '''
        More information related to the implementation
        of the convex hull algorithms can be found
        in the second part(2.Description of the solution and
        problem) of the attached paper titled
        Convex Hulls from Line Intersections: An In-Depth Comparative Study
    '''
    def orient(self, a, b,c):
        e = 1e-6
        ax,ay=a
        bx,by=b
        cx,cy=c
        val=(bx-ax)*(cy-ay)-(cx-ax)*(by-ay)
        if abs(val)<e:
            return 0 #Collinear
        return 1 if val>0 else -1 #1 CCW=left -1 CW

    def dst(self, a, b):
        ax,ay=a
        bx,by=b
        return (bx-ax)**2+(by-ay)**2
    #Jarvis March
    def lmPoint(self, inter):
        min=0
        for i in range(1, len(inter)):
            inter_x,inter_y=inter[i]
            min_x,min_y=inter[min]
            if inter_x<min_x:
                min=i
            elif inter_x==min_x and inter_y>min_y:
                min=i
        return min
    #@timed
    def jarvis(self, points):
        min=self.lmPoint(points)
        p_left=points[min]
        convex_hull=[]
        curr_p=p_left
        while True:
            convex_hull.append(curr_p)
            p_next=points[0]
            for p in points:
                if p!=curr_p:
                    turn=self.orient(curr_p,p,p_next)
                    if turn==1 or (turn==0 and self.dst(curr_p, p) > self.dst(curr_p, p_next)):
                        p_next=p
            curr_p=p_next
            if curr_p==p_left: #we close the hull
                break
        return convex_hull

    #Graham's scan
    def low_yPoint(self, points):
        min=0
        for i in range(1, len(points)):
            inter_x,inter_y=points[i]
            min_x,min_y=points[min]
            if inter_y<min_y:
                min=i
            elif inter_y==min_y and inter_x>min_x:
                min=i
        return min
    def polar_ang(self, p, q):
        angl=nmp.arctan2(q[1] - p[1], q[0] - p[0])
        dist=self.dst(p, q)
        return (angl,dist)
    #@timed
    def grahams(self, points):
        min=self.low_yPoint(points)
        p0=points[min]
        #sort based on polar angle in counterclockwise order around p0
        sorted_pt = sorted(points, key=lambda p: self.polar_ang(p0, p))
        hull=[p0,sorted_pt[0],sorted_pt[1]]
        for point in sorted_pt[2:]:
            while len(hull)>=2 and self.orient(hull[-2], hull[-1], point)!=1:
                 hull.pop()
            hull.append(point)
        return hull
    #Andrews variant of the Graham Scan
    #@timed
    def andrews_ver(self, points):

        points=sorted(points)
        lower=[]
        for p in points:
            while len(lower)>=2 and self.orient(lower[-2], lower[-1], p)!=1:
                lower.pop()
            lower.append(p)
        upper=[]
        for p in reversed(points):
            while len(upper)>=2 and self.orient(upper[-2], upper[-1], p)!=1:
                upper.pop()
            upper.append(p)
        return lower[:-1]+upper[:-1] #to create the hull=>concatenate lower and upper but both without the last elements


    def vis_ch(self):
        if len(self.convex_hull) > 1:
            hscreen = turtle.Turtle()
            hscreen.speed(0)#Change this to 2 when presenting
            hscreen.color("red")
            hscreen.pensize(2)
            hscreen.penup()
            hscreen.goto(self.convex_hull[0])
            hscreen.pendown()
            for point in self.convex_hull[1:]:
                hscreen.goto(point)
            hscreen.goto(self.convex_hull[0])
    def __init__(self, inter, ch):
        self.convex_hull=[]
        if ch==1:
            self.convex_hull=self.jarvis(inter)
        elif ch==2:
            self.convex_hull = self.grahams(inter)
        elif ch==3:
            self.convex_hull= self.andrews_ver(inter)
        self.vis_ch()


