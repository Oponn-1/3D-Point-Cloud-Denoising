"""
Function evaluate_registration calculates two main metrics. 
fitness measures the overlapping area (# of inlier correspondences / # of points in target). Higher the better. 
inlier_rmse measures the RMSE of all inlier correspondences. Lower the better.

optimal: fitness > 0.60 and inlier_rmse < 0.01
same: fitness = 1 inlier_rmse = 0
ref: http://www.open3d.org/docs/tutorial/Basic/icp_registration.html
"""

from open3d import * 
import copy


# onshow 
def paint(input_path):
    source = read_point_cloud(input_path)
    print(source)
    source_temp = copy.deepcopy(source)
    source_temp.paint_uniform_color([1, 0.706, 0])
    draw_geometries([source_temp])


def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    draw_geometries([source_temp, target_temp])


def _metrics_eval(source, target, threshold, trans_init):
    # draw_registration_result(source, target, trans_init)
    print("Initial alignment")
    evaluation = evaluate_registration(source, target,
            threshold, trans_init)
    print(evaluation)

    # can ignore by comments 
    # print("Transformation is:")
    # print(evaluation.transformation)
    # print("")


def _p2p_icp(source, target, threshold, trans_init):
    print("Apply point-to-point ICP")

    reg_p2p = registration_icp(source, target, threshold, trans_init,
            TransformationEstimationPointToPoint())  # default 30 iter
    # reg_p2p = registration_icp(source, target, threshold, trans_init,
    #     TransformationEstimationPointToPoint(),
    #     ICPConvergenceCriteria(max_iteration = 2000))

    print(reg_p2p)

    # can ignore by comments 
    print("Transformation is:")
    print(reg_p2p.transformation)
    print("")
    # draw_registration_result(source, target, reg_p2p.transformation)


def _p2l_ecp(source, target, threshold, trans_init):
    # assume no normalized point 
    estimate_normals(source, search_param = KDTreeSearchParamHybrid(
            radius = 0.1, max_nn = 30))  # default 
    estimate_normals(target, search_param = KDTreeSearchParamHybrid(
            radius = 0.1, max_nn = 30))
    # draw_geometries([source])  # test on normals 

    # need normalized point, notion inplace normailization 
    print("Apply point-to-plane ICP")

    reg_p2l = registration_icp(source, target, threshold, trans_init,
            TransformationEstimationPointToPlane())  # default 30 
    # reg_p2l = registration_icp(source, target, threshold, trans_init,
    #     TransformationEstimationPointToPlane(),
    #     ICPConvergenceCriteria(max_iteration = 2000))  # long long 

    print(reg_p2l)

    # can ignore by comments 
    print("Transformation is:")
    print(reg_p2l.transformation)
    print("")

    # draw_registration_result(source, target, reg_p2l.transformation)


def icp_eval(source, target):
    threshold = 0.02  # default 

    # no trans 
    trans_init = np.asarray(
                [[1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]])

    # _metrics_eval(source, target, threshold, trans_init)  # not icp but eval ok 
    _p2p_icp(source, target, threshold, trans_init)
    _p2l_ecp(source, target, threshold, trans_init)


# input 2 files 
def load_xyz(source_file_path, target_file_path):
    source = read_point_cloud(source_file_path)
    target = read_point_cloud(target_file_path)
    return source, target


# local demo 
def test():
    #### CREDIT: testing point cloud files from the IDETC paper #### 
    source_path = './TestData/15.xyz'
    target_path = './TestData/15_slight.xyz'  # delete few head lines 
    # target_path = './TestData/15.xyz'  # same  
    # target_path = './TestData/16.xyz'  # unmatched dataset try it out 

    source, target = load_xyz(source_path, target_path) 
    icp_eval(source, target)


if __name__ == "__main__":
    # python3 task_icp.py 
    test()


"""
quick helper
from task_icp import * 
# from task_icp import load_xyz, icp_eval, draw_registration_result, paint

source, target = load_xyz(source_path, target_path) # in xyz format plz 
icp_eval(source, target)
"""
