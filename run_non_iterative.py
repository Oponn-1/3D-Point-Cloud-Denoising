from scipy.spatial import Delaunay
import numpy as np
import math
from cloud_to_gts import input_triangulation
from cloud_to_gts import gts_write


def run_non_iterative():
    
    print("-----------------------------------------------------------")
    print("Running Non-Iterative, Feature Preserving Mesh Smoothing...")

    arg1 = input("sigma_f: ")
    arg2 = input("sigma_g: ")

    print()
    print("Probability distribution options:")
    print("1: Gaussian")
    print("2: Exponential")
    print("3: Gamma")
    dist_mode = input("selection: ")

    tri, points = input_triangulation()
    gts_in = gts_write(tri, points)

    in_file = gts_in
    out_file = input("Output GTS filename: ")

    with open(in_file, 'r') as f:
        with open(out_file, 'w') as o:
            subprocess.run(["./smoother", arg1, arg1, dist_mode], stdin=f, stdout=o)
    


run_non_iterative()
