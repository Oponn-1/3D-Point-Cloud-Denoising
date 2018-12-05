import os

test_files = ["bunny_bms_denoised.xyz", "bunny_nims_smoothed.xyz", "bunny_mesh.gts", "bunny_smooth.gts"]
for f in test_files:
    if os.path.exists(f):
        os.remove(f)
