import numpy as np
from scipy.spatial import Delaunay
import math


'''
Function:   input_triangulation()
Use:        return Delaunay triangulation of input .xyz file
'''
def input_triangulation():
    filename = raw_input("Input file name: ")

    f = open(filename, 'r')

    p = []

    # Read points from the file into numpy array
    for l in f:
        row = l.split()
        p.append([row[0], row[1], row[2]])
        # in case there are two 'columns' in the file
        if (len(row) == 6):
            p.append([row[3], row[4], row[5]])

    points = np.array(p)

    print("Points Loaded")

    tri = Delaunay(points[:-1], qhull_options="Qbb Qc Qz Q12 QJ Qt")

    print("Triangulation Complete")

    return tri, points;


'''
Function:   gts_write()
Use:        convert point cloud into gts file for non iterative
            algorithm execution
'''
def gts_write(tri, points):

    filename = raw_input("GTS file name: ")

    num_points = points.shape[0]
    

    f = open(filename, 'w')

    f.write("gtsfile")


