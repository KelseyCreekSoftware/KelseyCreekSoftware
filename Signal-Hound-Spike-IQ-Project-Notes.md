# Signal Hound Spike IQ Project Notes

Validate:
DataType – Should be Complex Short indicating the binary format of the binary IQ file. 

Convert and Store:
CenterFrequency of data capture, for example 100000000.000
SampleCount – Number of IQ values stored in the IQ binary file.
EpochNanos – Nanoseconds elapsed since January 1, 1970 to the first sample in the IQ waveform 
acquisition.  Unix epoch timestamp. 

Annotations:
SampleRate – Sample rate in Hz, of the IQ waveform acquisition. 
IFBandwidth – Cutoff frequency of the IQ bandpass filter. 
ScaleFactor – Used to scale the IQ data from full scale to mW. 
Decimation – Power of two integer value representing the decimation rate of the IQ waveform 
from the full sample rate of the receiver. For example, 40MS/s for the BB60C 
ReferenceLevel – The reference level, in dBm, set in the Spike software for the acquisition. 
DeviceType – Signa Hound device type, for example BB60C
SerialNumber – Serial number of the device used in acquisition. 
IQFileName – Full file path of the IQ binary file saved by the Spike software on the originating system. 
