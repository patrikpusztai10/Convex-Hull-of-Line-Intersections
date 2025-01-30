import random
import os
import turtle
import psutil
from horology import timed
from sortedcontainers import SortedList
from memory_profiler import profile
from convexhull import ConvexHull
class LineIntersection:
    '''
           More information related to the implementation
           of the line intersection algorithms can be found
           in the second part(2.Description of the solution and
           problem) of the attached paper titled
           Convex Hulls from Line Intersections: An In-Depth Comparative Study
    '''
    def create_lines(self, minx, maxx, miny, maxy, nr):
        self.screen.setworldcoordinates(minx, miny, maxx, maxy)
        nr=int(nr)
        tlines = turtle.Turtle()
        tlines.speed(0)
        tlines.hideturtle()
        while len(self.lines)<nr:
            x1,y1 = random.randint(minx,maxx),random.randint(miny, maxy)
            x2,y2 = random.randint(minx,maxx),random.randint(miny, maxy)
            sc = tlines.getscreen()
            sc.tracer(0)
            if (x1, y1, x2, y2) not in self.lines and (x1 != x2 or y1 != y2):
                self.lines.append((x1, y1, x2, y2))
                tlines.penup()
                tlines.goto(x1, y1)
                tlines.pendown()
                tlines.goto(x2, y2)
            sc.update()
            sc.tracer(1)

            if (x1, y1, x2, y2) not in self.lines and (x1 != x2 or y1 != y2):
                self.lines.append((x1, y1, x2, y2))


    def destroy_root(self):
        self.root_destroy()

    def inter_cram(self, Ax, Ay, Bx, By, Cx, Cy, Dx, Dy):

        a1=By-Ay
        b1=Ax-Bx
        c1=a1*Ax +b1*Ay
        # Line 1: a1x + b1y = c1
        a2 =Dy -Cy
        b2=Cx-Dx
        c2=a2*Cx + b2*Cy
        # Line 2: a2x + b2y = c2
        det=a1*b2 - a2*b1
        if det!=0:
            x =(c1*b2-c2*b1)/det
            y =(a1*c2-a2*c1)/det
            if (min(Ax, Bx)<=x<=max(Ax, Bx) and min(Ay, By)<=y<=max(Ay, By) and
                    min(Cx, Dx)<=x<=max(Cx, Dx) and min(Cy, Dy)<=y<= max(Cy, Dy)):
                return (x,y)
        return False

    def on_seg(self, p, q, r):
        px,py=p
        qx,qy=q
        rx,ry=r
        return min(px, rx)<=qx<= max(px, rx) and min(py, ry)<=qy<=max(py,ry) #verifies whether q is on the segment pr
    def orient(self, a, b, c):
        #epsilon was necessary because often times the points are very close to eachother
        e = 1e-6
        ax,ay=a
        bx,by=b
        cx,cy=c
        val=(bx-ax)*(cy-ay)-(cx-ax)*(by-ay)
        if abs(val)<e:
            return 0 #Collinear
        return 1 if val>0 else -1 #1 CCW -1 CW
    def interSL(self, l1, l2):

        p1,q1=(l1[0], l1[1]),(l1[2], l1[3])
        p2,q2=(l2[0], l2[1]),(l2[2], l2[3])
        # check all possible cases o1,o2,o3 and o4
        o1=self.orient(p1, q1, p2)
        o2=self.orient(p1, q1, q2)
        o3=self.orient(p2, q2, p1)
        o4=self.orient(p2, q2, q1)

        if o1!= o2 and o3!= o4:
            return self.inter_cram(*l1, *l2)

        if o1==0 and self.on_seg(p1, p2, q1):
            return p2
        if o2==0 and self.on_seg(p1, q2, q1):
            return q2
        if o3==0 and self.on_seg(p2, p1, q2):
            return p1
        if o4==0 and self.on_seg(p2, q1, q2):
            return q1
        return False

    #Line intersections algorithms
    #@profile
    def cramers(self):
        for i,(Ax,Ay,Bx,By) in enumerate(self.lines):
            for Cx,Cy,Dx,Dy in self.lines[i + 1:]:
                inter= self.inter_cram(Ax, Ay, Bx, By, Cx, Cy, Dx, Dy)
                if inter:
                    self.inter_pt.add(inter)
    #@profile
    def bent_ott(self):
        events=[]
        for i, (x1, y1, x2, y2) in enumerate(self.lines):
            events.append((min(x1, x2), 'start', i)) # The segment starts here
            events.append((max(x1, x2), 'end', i)) # The segment ends here
        events.sort(key=lambda e: (e[0], e[1] == 'end'))
        active_segments=SortedList() #active segments= segments which haven't ended
        sl_inter=[]
        for x,eType,index in events:
            if eType=='start':
                for i_act in active_segments:
                    inter=self.interSL(self.lines[index], self.lines[i_act])
                    if inter:
                        sl_inter.append(inter)
                active_segments.add(index)
            elif eType=='end':
                active_segments.remove(index)
            self.inter_pt = sl_inter
    def __init__(self,root_destroy,minx,maxx,miny,maxy,nr,li,ch):
        self.root_destroy=root_destroy
        self.destroy_root()
        self.screen=turtle.Screen()
        self.lines=[]
        self.screen.setup(width=0.9, height=0.9)
        self.screen.title("Convex hull construction")
        self.inter_pt=set() # set=we will have unique values
        self.create_lines(minx,maxx,miny,maxy,nr)
        if li==1:
            self.cramers()
        if li==2:
            self.lines.sort(key=lambda line: min(line[0], line[2]))
            self.bent_ott()
        l_screen = turtle.Turtle()
        l_screen.speed(0)
        l_screen.shape("circle")
        l_screen.shapesize(0.3, 0.3)
        l_screen.color("blue")
        l_screen.penup()
        screen = l_screen.getscreen()
        screen.tracer(0) 
        for x, y in self.inter_pt:
            l_screen.goto(x, y)
            l_screen.stamp()
        screen.update()
        screen.tracer(1)
        ConvexHull(list(self.inter_pt), ch)
