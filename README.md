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
When running the Non-Iterative method with user input, you will be prompted to name two GTS files. These are simply the mesh files that are generated during the process, the first is passed into the smoother, and the second is the output of the smoother. This is automatically converted to .xyz, which you are also prompted to name. 

#### Parameters
The parameters will depend to some degree on the individual point cloud. However, based on our testing with the bunny dataset, the following are good parameters for each algorithm.

Bilateral Mesh Smoothing:
- Iterations: 2
- Subsampling: 10
- Neighbor Range: 2

Non Iterative Feature Preserving Mesh Smoothing:
- Distribution: Exponential
- Subsampling: 5
- Sigma_f: 2
- Sigma_g: 2

### Iterative Closest Point
To run ICP on two .xyz files:
```bash
python3 run_icp.py
```

> When prompted for a filename, always include the extension (it will either be .xyz or .gts, the prompt will tell you).

## INCLUDED DATASETS
The package includes six .xyz files for testing. 
- bunny.xyz 
- bunny_noisy.xyz 
- dragon.xyz 
- dragon_noisy.xyz 
- dog.xyz 
- dog_noisy.xyz

Each pair of point clouds includes a base point cloud and a noisy version, named respectively. The bunny point clouds are the default used for the automated test. The artificial noise applied to the base point clouds to generate the noisy verisons was simply a random (and limited) vertex displacement.

## TO-DO 
- [X] Write file conversion (.xyz to .gts)
- [X] Choose / Implement ICP 
- [X] Write overall execution script
- [X] Compile the smoother.c to MacOS 
- [ ] Compile the smoother.c to Windows
