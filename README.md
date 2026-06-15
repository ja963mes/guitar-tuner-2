# Guitar Tuner App

This is a very basic, bare bones guitar tuner application designed for assisting an indivdual with tuning their guitar. The application requires the machine to have a micripohne, which the application will automatically recognize. When the user strums the string, the microphone automatically detects the acoustic signal which is then processed through a YIN algorithm. This algorithm provides the application signal accuracyly while limiting background noise interference, thus allowing it to isolate only the intended audio signal. After audip processing, the frequency is converted to it's corresponding pitch notation. The intended frequency and pitch notation are displayed in the gui as well as the real time frequency of the audio signal from the guitar. this give the user a point of refrence to allow them to determine wither the string is to tight to loose to produce the intended note. 


### Run GuitarTuner with Python
First you need to install the necessary libraries.
* pip install numpy scipy sounddevice
Then from the terminal you can do:
* python gui.py

