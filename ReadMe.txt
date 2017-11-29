This application does the basic work of parsing a fit file, using the include open source
python-fitparse library to capture the power channel as an offset from start.

FIT File Background
------------------------------------------------------------------------------------------
The FIT file format, developed by Dynastream, is a common format used by fitness devices
to store fitness data. The format is message based, with each message having a timestamp
and one or more data "channels" depending on the device and accessories being used.

Channel data may include GPS, heart rate, power, distance or speed to name a few common
ones. When paired with a power meter, FIT messages are sampled at a constant rate, typically
once every second.

A single file will contain multiple channels and each channel has different data and 
data structures (byte, ushort, etc.)


Python
------------------------------------------------------------------------------------------
To run this application from a terminal, you need Python 2.7 or Python 3 and virtualenvironment

On Windows (Powershell):

virtualenv venv
.\venv\scripts\activate.ps1
pip install lib\fitparse-1.0.1.zip
python src\main.py .\data\2012-05-31-11-17-12.fit

On Linux:
virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
python ./src/getmaxaverage.py ./data/2012-05-31-11-17-12.fit

