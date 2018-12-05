# 3D-Point-Cloud-Denoising
Scripts to denoise point clouds

## QUICKSTART
To install all the necessary python packages:
```bash
pip install -r requirements.txt
```

To run an automated test that will check if everything is working:
```bash
python3 auto_test.py
```

To clean up all the extra files created by the test:
```bash
python3 test_cleanup.py
```

To run denoising with user input:
```bash
python3 denoise.py
```

To run ICP:
```bash
python3 run_icp.py
```

Always use file extensions when prompted for a filename (it will either be .xyz or .gts, the prompt will tell you).

## TO-DO 
- [X] Write file conversion (.xyz to .gts)
- [X] Choose / Implement ICP 
- [X] Write overall execution script
- [ ] Compile the smoother.c to MacOS & Windows executables
