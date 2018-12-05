from ICPEval import *

# from task_icp import load_xyz, icp_eval, draw_registration_result, paint, metrics_eval, p2p_icp, p2l_icp, init_para

source, target = load_xyz('1.xyz', '1_clean.xyz') # in xyz format plz 
threshold, trans_init = init_para()
icp_eval(source, target, threshold, trans_init)

