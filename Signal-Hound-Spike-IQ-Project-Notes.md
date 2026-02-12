# Signal Hound Spike IQ Project Notes

*Updated 2-12-2026*

## Code status

- Have moved stand alone code into local copy of sigmf code tree to integrate into convert command line __main__.py.
- Have reviewed all 1408 lines of sigmffile.py to better understand intergration when coding a converter.
- Need to locate multi channel IQ file to see how it is structured and determine how to convert to SigMF archive format.

## Resources

Spike-User-Manual.pdf - https://signalhound.com/sigdownloads/Spike/Spike-User-Manual.pdf

A GNU Radio OOT module for Signal Hound Devices - gr-signal-hound 

https://github.com/SignalHound/gr-signal-hound

## XML Signal Attributes

Validate:

* DataType – Should be Complex Short indicating the binary format of the binary IQ file. 

Convert and Store:

* CenterFrequency of data capture, for example 100000000.000
* SampleCount – Number of IQ values stored in the IQ binary file.
* EpochNanos – Nanoseconds elapsed since January 1, 1970 to the first sample in the IQ waveform 
acquisition.  Unix epoch timestamp. 
* DeviceType – Signa Hound device type, for example BB60C
* SampleRate – Sample rate in Hz, of the IQ waveform acquisition. 

Annotations:
* IFBandwidth – Cutoff frequency of the IQ bandpass filter. 
* ScaleFactor – Used to scale the IQ data from full scale to mW. 
* Decimation – Power of two integer value representing the decimation rate of the IQ waveform 
from the full sample rate of the receiver. For example, 40MS/s for the BB60C 
* ReferenceLevel – The reference level, in dBm, set in the Spike software for the acquisition. 

* SerialNumber – Serial number of the device used in acquisition. 
* IQFileName – Full file path of the IQ binary file saved by the Spike software on the originating system. 

Notes on data conversion from the Spike User Manual

The binary file contains SampleCount signed 16-bit IQ values. The binary file has little-endian byte 
ordering. Samples are stored in sequential order as: 

`I1, Q1, I2, Q2 … In, Qn` 

The values are stored as full scale, ranging from -32768 to +32767 representing floating point values 
between -1.0 and 1.0. To recover the original values, perform the following steps.

1) Read in the binary file to signed 16-bit complex values. 
2) Convert the full scale 16-bit I and Q integer values into floating point values in the range of -1.0 to 
+1.0. 
3) Multiply each I and Q value by the inverse of the scale factor in the XML file. 
4) The IQ samples should now be scaled to mW, where I2 + Q2 = mW.
 
