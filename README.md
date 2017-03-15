# rpi-get-temps

This repo builds a docker container that can be run to read temperatures from the gpio pins on a Raspberry Pi and stores them in a Firebase database

Requirements:
- Firebase database 
- A unique auth.uid to use to write to Firebase database
- A secret token from Firebase 
- An APIXU account with API Key

These values needs to be loaded into `envvals`

