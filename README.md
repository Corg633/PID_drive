# PID_drive
Basic code for Differential Drive platform to follow the line. Educational demo was developed for Mayflower S.T.E.M. Academy sessions.

![Robo_Front](https://github.com/user-attachments/assets/b47a267d-74b2-4c02-9f3d-8820abeeda4b)
![Robo  Bottom](https://github.com/user-attachments/assets/5f3aaf00-db08-4274-9430-9cfc43296ea6)

# Demo

https://github.com/user-attachments/assets/b62e2fe1-5da9-43dd-88be-5650a3f0bf1d

# Prerequisites

## Hardware:
Raspberry Pi 4, Model B.

## Software: 
- System: Raspberry Pi OS (x64)
- Kernel version: 6.6
- Debian version: 12 (bookworm)

## Libraries: 
- RPI.GPIO: Built-in Raspberry OS
- pigipio: Installation guide: https://abyz.me.uk/rpi/pigpio/download.html

# Project's Description

## PWM generation for DC Motors and H-bridge:
Short illustration:

![image](https://github.com/user-attachments/assets/51e4f7cf-f50f-4397-be0b-229a5920e037)
![image](https://github.com/user-attachments/assets/6d8dc582-8cac-4a46-adae-402458cff695)

Full guide and reference: https://www.ti.com/lit/ab/sboa174d/sboa174d.pdf?ts=1722116467092&ref_url=https%253A%252F%252Fwww.google.com%252F

## Encoder library:
Reference class to decode a rotary encoder to study and apply by link: https://abyz.me.uk/rpi/pigpio/examples.html#Python_rotary_encoder_py

Short illustration:

![image](https://github.com/user-attachments/assets/e659ba3d-a50c-469e-a44c-fd256334c0c4)
![image](https://github.com/user-attachments/assets/2cb119a8-9744-4f25-8f23-18c501162912)

Full guide and reference: https://makeatronics.blogspot.com/2013/02/efficiently-reading-quadrature-with.html

# PID setup:

PID controller for Left(L) and Right(R) Motors with Encoders in action:

https://github.com/user-attachments/assets/f242beac-2ccc-46d6-b5cc-def5a069c993

Capture of output and set point values for PID controllers of R and L Motors:

![Figure_PID_super](https://github.com/user-attachments/assets/19387b4a-a321-4cab-af17-656ab1474b06)

Capture with Logic Analyser of generated and recieved signals for H-bridge Motor Driver and for Rotary Encoder:

![PWM_ENC1](https://github.com/user-attachments/assets/895d398e-8ad9-46f9-bad9-733c3b6ee8a6)


## Connection Diagram (In Progress):
![diagram](https://github.com/user-attachments/assets/868966c1-4a45-424f-b1ee-3386dddcd071)

# Features
Developed Differential Drive Platrform has Intel Realsense Camera and deployed ORB_SLAM3 algorithm. Link: (https://github.com/UZ-SLAMLab/ORB_SLAM3).

Captured instance of estimated pose by ORB-SLAM3 algorithm:

![20240724_190209](https://github.com/user-attachments/assets/ae9a795f-8339-4a6a-80f4-2724bda85333)

