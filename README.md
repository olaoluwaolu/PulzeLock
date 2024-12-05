# PulzeLock
Today, fingerprint authentication systems are still susceptible to biometric spoofs. One way to combat this is to check for signs of liveness in users. Photoplethysmography (PPG; the same biosignals used in smartwatches to estimate heart rate) signals are the optimal solution for proving liveness since they can be used to estimate heart rate, oxygen saturation or breathing rate. More interestingly, since an individual's PPG signal is largely influenced by their cardiovascular system, a user's PPG signal is unique to them.

PulzeLock is an early prototype of a device capable of estimating heart rate, breathing rate, and oxygen saturation using a user's PPG signal. The system also uses the PPG signal to authenticate enrolled users into the system  

![image](https://github.com/user-attachments/assets/e8924b16-973c-4c70-b791-46fb9add8a88)

# Hardware Schematic

![image](https://github.com/user-attachments/assets/5a2d26fb-f585-448d-b378-17aca690949c)

# Theory - Vital Signs Extraction

Vital sign extraction is built around the method of using standard RGB video to act as a light-based pulse oximeter. A light is shown through the finger to illuminate the finger and a camera is used to record the change in light intesnity over time to create a photopthelysmogram.
![image](https://github.com/user-attachments/assets/4a080818-9605-46e4-bff2-b64f43495168)

![image](https://github.com/user-attachments/assets/4b78aae6-d9e1-40ac-9eab-ceb596b92426)

- /-- Logan: try to mainly use pictures/figures and little text to explain it if possible

## Heart Rate

## Breathing Rate

## SpO2

# Theory - User Identification

/--Olaolu: Include the User ID pipeline + explain the reasoning + hyperparameters

# Future Work

Currently, our proposed algorithm for user identification via deep learning is unable to distinguish between users. Future work to improve this includes:
+ Developing an improved deep-learning algorithm for identification
+ Collecting longer PPG recordings (>1 minute)

# Files + Description
- python_PPG.py: This file takes the filepath of the video and the state of the system. This script processes the video into an array of values creating the PPG signal. Additionally it calculates the HR, SP02, and RR vital signs, storing the ouptut into a txt file. It then stores the PPG signal as a JSON to be used by other scripts later. 
- RaspiIDv2.py: The purpose of this file is to
- button_hnadler.sh: Polls GPIO pins to detect a button press. Updates the state of the system and calls system_control.sh
- system_control.sh: Calls camera_script.sh, passes filepath argument to python_PPG.py script and system state as an argument. Calls RaspiIDv2.py
- camera_script.sh: JONAS
- I2C_OLED.py: JONAS
- requirements.txt: Contains the required python packages to be installed
- activate.txt: Setups the python enviroment and installs the packages listed in 'requirements.txt'
# Steps to run the system

First: Move all 'pulzelock_main' files onto the Raspberry Pi device.
Second: run ./activate.sh from the folder containing all of the system files.
Third: run ./button_handler.sh 

Ensure all files are in the same main directory.
