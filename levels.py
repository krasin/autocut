#!/usr/bin/python

import ocl
import camvtk
import time
import vtk
import math
import area

class TriangleProcessor(object):
    def __init__(self, tr):
        self.p = tr.getPoints()
        self.low = min(p.z for p in self.p)
        self.high = max(p.z for p in self.p)
        self.n = tr.n

    def Horizontal(self):
        if self.n.z < 0:
            return False
        return self.high - self.low >= 0 and self.high - self.low < 0.05

    def Vertical(self):
        d = self.n.dot(ocl.Point(0,0,1))
        return abs(d) < 0.01

    def Level(self):
        return self.low

def seq(pl):
    ret = []
    for p in pl:
        ret.append([p.x, p.y, p.z])
    return ret

def drawLoops(myscreen, loops):
    points = []
    for loop in loops:
        for p in loop:
            points.append(p)
    myscreen.addActor(camvtk.PointCloud(points))

def IsNegative(prev, vertex):
    p1 = prev - vertex.c
    p2 = vertex.p - vertex.c

    smaller_angle_ccw = (p1 ^ p2 > 0)
    if vertex.type == 1:  # CCW arc, positive iff smaller angle is CCW
        return smaller_angle_ccw
    else:  # CW arc, positive if smaller angle is CW
        return not smaller_angle_ccw

def drawCurve(myscreen, curve, z):
    vertices = curve.getVertices()
    current = vertices[0].p
    print "start at (%.2f, %.2f) z=%.2f" % (current.x, current.y, z)
    for v in vertices[1:]:
        if v.type == 0:
            print "line to (%.2f,%.2f) z=%.2f" % (v.p.x, v.p.y, z)
            myscreen.addActor(camvtk.Line(p1=(current.x, current.y, z), p2 = (v.p.x, v.p.y, z)))
        else:
            r = math.hypot(v.p.x-v.c.x, v.p.y-v.c.y)
            print "arc to (%.2f,%.2f) center=(%.2f,%.2f) r=%.2f z=%.2f" % (v.p.x, v.p.y, v.c.x, v.c.y, r, z)
            src = vtk.vtkArcSource()
            src.SetCenter(v.c.x, v.c.y, z)
            src.SetPoint1(current.x, current.y, z)
            src.SetPoint2(v.p.x, v.p.y, z)
            src.SetResolution(20)
            src.SetNegative(not IsNegative(current, v))
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(src.GetOutput())
            actor = camvtk.CamvtkActor()
            actor.SetMapper(mapper)
            myscreen.addActor(actor)
        current = v.p

            
kTop = 14
kBottom = 2
kStepDown = 1
kStepOver = 1
kVerticalTolerance = 0.05
kToolDiameter = 3.175

kFilename = "wheel-rim.stl"
kRotate = (0, -90, 0)

def GetEssentialLevels(s):
    levels = []
    good = 0
    total = 0
    for t in s.getTriangles():
        tr = TriangleProcessor(t)
        total += 1
        if tr.Horizontal():
            levels.append(tr.Level())
            good += 1
        elif tr.Vertical():
            good += 1
        else:
            p = seq(t.getPoints())
    print "good=", good, " total=", total

    levels.sort()
    print levels
    essential_levels = []
    i = 0
    while i < len(levels):
        l0 = levels[i]
        j = i+1
        while j < len(levels):
            l1 = levels[j]
            if l1 > l0 + 0.1:
                break
            j += 1
        essential_levels.append(l0)
        i = j
    essential_levels.sort(reverse=True)
    essential_levels = [l for l in essential_levels if l >= kBottom]
    if len(essential_levels) == 0 or essential_levels[len(essential_levels) - 1] != kBottom:
        essential_levels.append(kBottom)

    return essential_levels

def GetWaterlines(s, essential_levels):
    cutter = ocl.CylCutter(kToolDiameter, 20)
    level_loops = []
    for l in essential_levels:
        print "level=", l
        wl = ocl.Waterline()
        wl.setSTL(s)
        wl.setCutter(cutter)
        wl.setSampling(0.02)
        wl.setZ(l)
        wl.run2()
        level_loops.append(wl.getLoops())

    return level_loops

def MakeArea(loops):
    ar = area.Area()
    for loop in loops:
        curve = area.Curve()
        for p in loop:
            curve.append(area.Point(p.x, p.y))
        ar.append(curve)
    ar.FitArcs()
    ar.Reorder()
    return ar

def ConvertLoopsToAreas(level_loops):
    ret = []
    for i, loops in enumerate(level_loops):
        print "Processing", i, "th level:"
        ar = MakeArea(loops)
        print "Area made"
        ret.append(ar)
    print "Done processing"
    return ret

def MakeCutAreas(levels, areas):
    outer_bound = area.Area(areas[len(areas) - 1])
    outer_bound.Offset(-3.175)
    cut_levels = [ kTop ]
    cut_areas = [ outer_bound ]
    for i, ar in enumerate(areas):
        for curve in outer_bound.getCurves():
            ar.append(curve)
        ar.Reorder()
        cut_areas.append(ar)
        cut_levels.append(levels[i])
    return cut_levels, cut_areas

def MakeLevelToolpaths(levels, areas):
    tps = []
    for i, ar in enumerate(areas):
        print "Making", i, "th toolpath at", levels[i]
        tp = ar.MakePocketToolpath(3.175, -3.175, kStepOver, True, False, 0)
        tps.append(tp)
        print " -- Got", len(tp), "curves"
    print "Out:", len(tps), "levels"
    return levels, tps

def MakeCompleteToolpath(tp_levels, tp_paths):
    cur_lev = tp_levels[0]
    cur_tp = tp_paths[0]
    next_levels_idx = 1

    levs = [ ]
    tps = [ ]
    while cur_lev > kBottom - kVerticalTolerance:
        levs.append(cur_lev)
        tps.append(cur_tp)

        cur_lev -= kStepDown

        if (next_levels_idx < len(tp_levels) and
            cur_lev < tp_levels[next_levels_idx] + kVerticalTolerance):
            cur_tp = tp_paths[next_levels_idx]
            cur_lev = tp_levels[next_levels_idx]
            next_levels_idx += 1
    return levs, tps

# def PopulateIntermediateLevels(essential_levels, level_loops):
#     last_loops = level_loops[len(level_loops)-1]

#     cut_levels = []
#     cut_loops = []
#     current = kTop
#     current_loops = last_loops
#     next_level_idx = 0
#     while current > kBottom - kVerticalTolerance:
#         cut_levels.append(current)
#         cut_loops.append(current_loops)
#         current -= kStepDown

#         if (next_level_idx < len(essential_levels) and
#             current < essential_levels[next_level_idx] + kVerticalTolerance/2):
#             cut_levels.append(essential_levels[next_level_idx])
#             cut_loops.append(current_loops)
#             if next_level_idx == len(essential_levels) - 1:
#                 current_loops = last_loops
#             else:
#                 current_loops = level_loops[next_level_idx] + last_loops
#             if current > essential_levels[next_level_idx] - kVerticalTolerance/2:
#                 current -= kStepDown
#             next_level_idx += 1

#     return cut_levels, cut_loops

# def MakePocket(loops, step):
#     ar = MakeArea(loops)
#     tp = ar.MakePocketToolpath(3.175, 0, step, True, False, 0)
#     return tp

if __name__ == "__main__": 
    print ocl.version()
    
    stl = camvtk.STLSurf(kFilename, color=camvtk.green)
    stl.SetOpacity(0.2)
    stl.RotateX(kRotate[0])
    stl.RotateY(kRotate[1])
    stl.RotateZ(kRotate[2])
    print "STL surface read"
    polydata = stl.src.GetOutput()
    s= ocl.STLSurf()
    camvtk.vtkPolyData2OCLSTL(polydata, s)
    s.rotate(kRotate[0] * math.pi / 180,
             kRotate[1] * math.pi / 180,
             kRotate[2] * math.pi / 180)
    bb = s.getBounds()
    sx = max(abs(bb[0]), abs(bb[1]))
    sy = max(abs(bb[1]), abs(bb[2]))
    ms = max(sx, sy)
    print "STLSurf with ", s.size(), " triangles"

    essential_levels = GetEssentialLevels(s)
    level_loops = GetWaterlines(s, essential_levels)

    for i, lev in enumerate(essential_levels):
        lengths = [str(len(loop)) for loop in level_loops[i]]
        print "L%02d@%smm: %s" % (i, lev, ",".join(lengths))

    # cut_levels, cut_loops = PopulateIntermediateLevels(essential_levels, level_loops)
    # print "------------------------"
    # print "cut levels: %d, cut_loops: %d" % (len(cut_levels), len(cut_loops))
    # for i, lev in enumerate(cut_levels):
    #     lengths = [str(len(loop)) for loop in cut_loops[i]]
    #     if i > 0:
    #         print "L%02d@%smm: %s (d=%s)" % (i, lev, len(lengths), cut_levels[i-1]-lev)
    #     else:
    #         print "L%02d@%smm: %s" % (i, lev, len(lengths))

    # print "------------------------"

    #    pocket_tps = [ MakePocket(loops, kStepOver) for loops in cut_loops ]
    #    pocket_tps = [ MakePocket(loops, kStepOver) for loops in level_loops]

    level_areas = ConvertLoopsToAreas(level_loops)
    cut_levels, cut_areas = MakeCutAreas(essential_levels, level_areas)
    tp_levels, tp_paths = MakeLevelToolpaths(cut_levels, cut_areas)
    tp_levels, tp_paths = MakeCompleteToolpath(tp_levels, tp_paths)

    myscreen = camvtk.VTKScreen()    
    myscreen.addActor(stl)

    for i, lev in enumerate(tp_levels):
       tp = tp_paths[i]
       print "Lev", i, "@", lev, ":", len(tp), "curves"
       for c in tp:
           drawCurve(myscreen, c, lev)
    # all_loops = []
    # for loops in level_loops:
    #     all_loops += loops
    # drawLoops(myscreen, all_loops)
    
    myscreen.camera.SetPosition(3, 23, 15)
    myscreen.camera.SetFocalPoint(5, 5, 0)
    myscreen.render()
    print " All done."
    myscreen.iren.Start()
