# PulzeLock
Today, fingerprint authentication systems are still susceptible to biometric spoofs. One way to combat this is to check for signs of liveness in users. Photoplethysmography (PPG; the same biosignals used in smartwatches to estimate heart rate) signals are the optimal solution for proving liveness since they can be used to estimate heart rate, oxygen saturation or breathing rate. More interestingly, since an individual's PPG signal is largely influenced by their cardiovascular system, a user's PPG signal is unique to them.

PulzeLock is an early prototype of a device capable of estimating heart rate, breathing rate, and oxygen saturation using a user's PPG signal. The system also uses the PPG signal to authenticate enrolled users into the system  

/--Add image of system---

# Hardware Schematic

/--add schematic---

# Theory - Vital Signs Extraction

Vital sign extraction is built around the method of using standard RGB video to act as a light-based pulse oximeter. A light is shown through the finger to illuminate the finger and a camera is used to record the change in light intesnity over time to create a photopthelysmogram.
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
- /-- Logan: can you add in any files that you used here? 
- RaspiIDv2.py: The purpose of this file is to
- File2.xyz - text

# Steps to run the system
