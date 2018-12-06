from scipy.spatial import Delaunay
import numpy as np
import math
from cloud_to_gts import gts_write
from cloud_to_gts import input_triangulation
from run_non_iterative import run_non_iterative
from BilateralMeshDenoising import run_bilateral_denoising
from run_icp import run_icp

def test_1():

    print()
    print("************************************")
    print("*      RUNNING AUTOMATED TEST      *")
    print("************************************")
    print()

    run_bilateral_denoising(True)
    print()
    print("BILATERAL MESH DENOISING is FUNCTIONAL")
    print()

    run_non_iterative(True)
    print()
    print("NON ITERATIVE FEATURE PRESERVING MESH SMOOTHING is FUNCTIONAL")
    print()

    run_icp(True)
    print()
    print("ICP is FUNCTIONAL")
    print()

    print("ALL TESTS PASSED")
    print()

test_1()
