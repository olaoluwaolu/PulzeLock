# PulzeLock
Today, fingerprint authentication systems are still susceptible to biometric spoofs. One way to combat this is to check for signs of liveness in users. Photoplethysmography (PPG; the same biosignals used in smartwatches to estimate heart rate) signals are the optimal solution for proving liveness since they can be used to estimate heart rate, oxygen saturation or breathing rate. More interestingly, since an individual's PPG signal is largely influenced by their cardiovascular system, a user's PPG signal is unique to them.

PulzeLock is an early prototype of a device capable of estimating heart rate, breathing rate, and oxygen saturation using a user's PPG signal. The system also uses the PPG signal to authenticate enrolled users into the system  

**Video Description**: https://www.youtube.com/watch?v=nMshs-2wH0M

<img src="https://github.com/user-attachments/assets/8f85869d-9372-4721-8a69-4964229d7417" alt="image" width="50%">



# Hardware Schematic
<img src="https://github.com/user-attachments/assets/5a2d26fb-f585-448d-b378-17aca690949c" alt="image" width="50%">


The used OLED screen (Adafruit SSD1306 128x64) can be purchased at:
https://www.adafruit.com/product/326

The used camera (Raspberry Pi Camera V2.1) can be purchased at:
https://www.raspberrypi.com/products/camera-module-v2/

# Theory - Vital Signs Extraction + User Identification
+ We start by recording an RGB video of the user's illuminated finger using our camera, and extract the intensity of light across all frames of the video. This yields the PPG signal.

+ With this PPG signal, we can either extract the vital signs (heart rate, oxygen saturation, and breathing rate) or proceed to determine who the signal belongs to using the algorithm in blue.

![image](https://github.com/user-attachments/assets/44cc7bd0-ea77-4179-867a-432c62a376c6)

# Files + Description
- **python_PPG.py**: This file extracts the PPG signal from the video recording taken on our camera. It takes the filepath of the video and the state of the system (vital signs mode or user identification mode). Additionally, it calculates the heart rate, oxygen saturation (SpO2), and breathing rate, storing the output into a text file. It then stores the PPG signal as a JSON file to be used by other scripts later.

- **RaspiIDv2.py**: This file loads the machine learning model, receives the JSON PPG signal as an input, and outputs the class that the signal belongs to. Based on the estimated class, it either welcomes the user or denies the user.

- **button_handler.sh**: Polls GPIO pins to detect a button press. Updates the state of the system and calls system_control.sh
  
- **system_control.sh**: Calls camera_script.sh, passes filepath argument to python_PPG.py script and the system state as an argument. Calls RaspiIDv2.py.

  
- **camera_script.sh**: Responsible for executing the command to record the actual video as well as simple user instructions related to video recording. The script itself has different modes, of which the most prominent one is "record", passed as an argument. The actual recording command "libcamera-vid" has two main arguments: specifying the recording length and file output path.

- **I2C_OLED.py**: Reads from output.txt and displays the contents to the OLED. This was developed based on example found at https://learn.adafruit.com/monochrome-oled-breakouts/python-usage-2 . Requires you to enter a virtual Python environment, to install the libraries "sys", "json", "time", "board", "digitalio", "pillow" and "adafruit_ssd1306".

- **requirements.txt**: Contains the required python packages to be installed

- **activate.txt**: Sets up the python enviroment and installs the packages listed in 'requirements.txt'

- **Update_Raspi_ID.py**: Contains neccessary code to run a deep learning model to train and validate the user identification pipeline. Training and validation uses 5-fold stratified cross-validation
 
# Future Work
Currently, our proposed algorithm for user identification via deep learning is unable to distinguish between users. Future work to improve this includes:
+ Developing an improved deep-learning algorithm for identification

+ Collecting longer PPG recordings (>1 minute)

## Updating The Deep Learning Model
To make any updates to the model, you must make updates to these file(s):

- **Update_Raspi_ID.py**: Simply make edits to create_model() function to update the deep learning method. This program takes a folder of JSON PPG signals (each PPG signal in the JSON file must be stored as an array). Ensure you update 'json_folder_path' to be a path to a folder with JSON PPG data. Once done, this will make a new '_ppg_model.h5_' file. This is your new AI model. Upload it to your Pi to use it.

# Steps to run the system

1. Move all 'pulzelock_main' files onto the Raspberry Pi device.

2. run ./activate.sh from the folder containing all of the system files.

3. run ./button_handler.sh 

Ensure all files are in the same main directory.
