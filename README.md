# 3D-Point-Cloud-Denoising
Python scripts to denoise point clouds and evaluate results.

This package provides implementations of two algorithms from recent literature. The Non Iterative Feature Preserving method has been enhanced with the inclusion of different probability distributions for weighting of the point shifts.

## SETUP INSTRUCTIONS
Download the repository as a zip file. Extract the package and go into the project directory. From there, perform the following to install all necessary python packages:
```bash
pip install -r requirements.txt
```

## RUNNING INSTRUCTIONS
### Automated Test
To run an automated test that will check if everything is working:
```bash
python3 auto_test.py
```

> When prompted to select your system, make sure to choose the right one. Currently only Linux and MacOS are supported. The prompt will list the available systems.

> When prompted to make any selection out of a numbered list of options, type the number as your response. 

To clean up all the extra files created by the test:
```bash
python3 test_cleanup.py
```

### User Controlled Execution
To run denoising with user input:
```bash
python3 denoise.py
```

### Iterative Closest Point
To run ICP on two .xyz files:
```bash
python3 run_icp.py
```

> When prompted for a filename, always include the extension (it will either be .xyz or .gts, the prompt will tell you).

## TO-DO 
- [X] Write file conversion (.xyz to .gts)
- [X] Choose / Implement ICP 
- [X] Write overall execution script
- [X] Compile the smoother.c to MacOS 
- [ ] Compile the smoother.c to Windows
