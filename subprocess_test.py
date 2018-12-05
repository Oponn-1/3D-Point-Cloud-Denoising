import subprocess

in_file = input("Input GTS: ")
out_file = input("Output GTS: ")

with open(in_file, 'r') as f:
	with open(out_file, 'w') as o:
		subprocess.run(["./smoother", "1", "1", "1"], stdin=f, stdout=o)

