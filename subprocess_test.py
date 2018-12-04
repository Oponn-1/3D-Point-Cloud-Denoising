import subprocess

f = open('bunny.gts', 'r')
o = open('bunny_smooth.gts', 'w')
subprocess.run(["./smoother", "1", "1", "1"], stdin=f, stdout=o)

