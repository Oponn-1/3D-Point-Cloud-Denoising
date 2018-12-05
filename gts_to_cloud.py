from cloud_to_gts import gts_to_cloud

gts_file = input("Target GTS filename: ")
xyz_file = input("New XYZ filename: ")

gts_to_cloud(gts_file, xyz_file)
