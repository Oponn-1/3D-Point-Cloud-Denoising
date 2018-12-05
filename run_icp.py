from task_icp import * 

# from task_icp import load_xyz, icp_eval, draw_registration_result, paint, metrics_eval, p2p_icp, p2l_icp, init_para

def run_icp(testing):
    print("----------------------")
    print("Running ICP comparison")
    print("----------------------")

    f1 = "bunny_bms_denoised.xyz"
    f2 = "bunny.xyz"

    if (not testing):
        f1 = input("xyz filename 1: ")
        f2 = input("xyz filename 2: ")

    # files must be in xyz format
    source, target = load_xyz(f1, f2)
    threshold, trans_init = init_para()
    icp_eval(source, target, threshold, trans_init)

