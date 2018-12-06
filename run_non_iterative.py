from scipy.spatial import Delaunay
import numpy as np
import math
import subprocess
from cloud_to_gts import input_triangulation
from cloud_to_gts import gts_write
from cloud_to_gts import gts_to_cloud


def run_non_iterative(testing):
    
    print("***********************************************************")
    print("RUNNING NON ITERATIVE, FEATURE PRESERVING MESH SMOOTHING...")
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
            system_id = 0
            print()
            print("********")
            print("0: Linux")
            print("1: MacOS")
            system_id = int(input("What system are you on? "))
            if (system_id == 1):
                subprocess.run(["./smoother_mac", arg1, arg2, dist_mode], stdin=f, stdout=o) 
            if (system_id == 0):
                subprocess.run(["./smoother", arg1, arg2, dist_mode], stdin=f, stdout=o)

    out_xyz = "bunny_nims_smoothed.xyz"
    if (not testing):
        out_xyz = input("Output XYZ filename: ")

    gts_to_cloud(out_file, out_xyz)

