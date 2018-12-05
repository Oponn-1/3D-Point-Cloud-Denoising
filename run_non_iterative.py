from scipy.spatial import Delaunay
import numpy as np
import math
import subprocess
from cloud_to_gts import input_triangulation
from cloud_to_gts import gts_write
from cloud_to_gts import gts_to_cloud


def run_non_iterative(testing):
    
    print("***********************************************************")
    print("Running Non-Iterative, Feature Preserving Mesh Smoothing...")
    print("***********************************************************")

    arg1 = "1"
    arg2 = "1"
    dist_mode = "1"

    if (not testing):
        arg1 = input("sigma_f: ")
        arg2 = input("sigma_g: ")

        print()
        print("Probability distribution options:")
        print("1: Gaussian")
        print("2: Exponential")
        print("3: Gamma")
        dist_mode = input("selection: ")

    tri, points = input_triangulation(testing)
    gts_in = gts_write(tri, points, testing)

    in_file = gts_in

    out_file = "bunny_smooth.gts" 
    if (not testing):
        out_file = input("Smoothed GTS filename: ")

    with open(in_file, 'r') as f:
        with open(out_file, 'w') as o:
            # todo decide the environment 
            # subprocess.run(["./smoother", arg1, arg1, dist_mode], stdin=f, stdout=o)
            subprocess.run(["./smoother_mac", arg1, arg1, dist_mode], stdin=f, stdout=o)  # for mac only

    out_xyz = "bunny_nims_smoothed.xyz"
    if (not testing):
        out_xyz = input("Output XYZ filename: ")

    gts_to_cloud(out_file, out_xyz)

