'''
Created on 29-Nov-2014

@author: deepa
'''
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere, \
    BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                BRepBuilderAPI_MakeVertex,
                                BRepBuilderAPI_MakeWire)
from OCC.Core.BRepFill import BRepFill_Filling
from OCC.Core.GeomAbs import GeomAbs_C0
from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.Quantity import Quantity_NOC_BLACK

    
def make_edge(*args):
    edge = BRepBuilderAPI_MakeEdge(*args)
    result = edge.Edge()
    return result


def make_vertex(*args):
    vert = BRepBuilderAPI_MakeVertex(*args)
    result = vert.Vertex()
    return result


def make_n_sided(edges, continuity=GeomAbs_C0):
    n_sided = BRepFill_Filling()
    for edg in edges:
        n_sided.Add(edg, continuity)
    n_sided.Build()
    face = n_sided.Face()
    return face


def make_wire(*args):
    # if we get an iterable, than add all edges to wire builder
    if isinstance(args[0], list) or isinstance(args[0], tuple):
        wire = BRepBuilderAPI_MakeWire()
        for i in args[0]:
            wire.Add(i)
        wire.Build()
        return wire.Wire()
    wire = BRepBuilderAPI_MakeWire(*args)
    return wire.Wire()


def points_to_bspline(pnts):
    pts = TColgp_Array1OfPnt(0, len(pnts) - 1)
    for n, i in enumerate(pnts):
        pts.SetValue(n, i)
    crv = GeomAPI_PointsToBSpline(pts)
    return crv.Curve()


def make_wire_from_edges(edges):
    wire = None
    for edge in edges:
        if wire:
            wire = make_wire(wire, edge)
        else:
            wire = make_wire(edge)
    return wire


def make_face_from_wire(wire):
    return BRepBuilderAPI_MakeFace(wire).Face()


def get_gp_pt(point):
    return gp_Pnt(point[0], point[1], point[2])


def get_gp_dir(direction):
    return gp_Dir(direction[0], direction[1], direction[2])


def make_edges_from_points(points):
    edges = []
    num = len(points)
    for i in range(num - 1):
        edge = make_edge(get_gp_pt(points[i]), get_gp_pt(points[i + 1]))
        edges.append(edge)

    cycle_edge = make_edge(get_gp_pt(points[num - 1]), get_gp_pt(points[0]))
    edges.append(cycle_edge)
    
    return edges


def make_prism_from_face(aFace, eDir):
    return BRepPrimAPI_MakePrism(aFace, gp_Vec(gp_Pnt(0., 0., 0.), gp_Pnt(eDir[0], eDir[1], eDir[2]))).Shape()
    # return BRepPrimAPI_MakePrism(aFace, gpDir, False).Shape()
