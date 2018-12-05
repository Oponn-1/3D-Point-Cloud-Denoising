import subprocess

with open('bunny.gts', 'r') as f:
	with open('bunny_smooth.gts', 'w') as o:
		subprocess.run(["./smoother", "1", "1", "1"], stdin=f, stdout=o)

