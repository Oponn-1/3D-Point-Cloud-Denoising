from scipy.spatial import Delaunay
import numpy as np
import math
from cloud_to_gts import input_triangulation
from cloud_to_gts import gts_write


def run_non_iterative():
    
    print()
    print("Running Non-Iterative, Feature Preserving Mesh Smoothing...")

    arg1 = int(input("sigma_f: "))
    arg2 = int(input("sigma_g: "))

    print("Probability distribution options:")
    print("1: Gaussian")
    print("2: Exponential")
    print("3: Gamma")
    dist_mode = int(input("selection: "))

    tri, points = input_triangulation()
    gts_write(tri, points)


run_non_iterative()
