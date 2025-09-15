# Rough Notes on IQ File Information

## HDF5

ITU-R SM.2117-0 is a data format definition for exchanging stored I/Q data with the intention of spectrum monitoring. Key Bridge Wireless supports the ITU in creating a library for the data format as a contribution to IEEE 1900.8 Working Group. This is an HDF5 read-write Python library for the data format in Recommendation ITU-R SM.2117-0.

https://pypi.org/project/itusm2117/

## NTIA


## Rohde and the other guy...

https://www.rohde-schwarz.com/us/applications/converting-r-s-i-q-data-files-application-note_56280-35531.html

### I/Q Data Import Export library (daiex)

Daiex is a cross-platform C++ library that provides functions to import and export numeric I/Q data to or from various file formats. The library provides standardized read and write functions that encapsulate all file operations. The following file formats are supported:

|File format| file extension | comment|
| --- | --- |:------------------------------|
| iq-tar|	.iq.tar | An iq-tar file contains I/Q data in binary format together with meta information that describes the nature and the source of data, e.g. sample rate. The objective of the iq-tar file format is to separate I/Q data from the meta information while still having both in one file. |
|IQW (IIIQQQ) |	.iqw |	A file that contains Float32 data in a binary format ( first all I values are stored, followed by all Q values ). The file does not contain any additional header information. Note that I and Q data are first buffered to temporary files and are merged when calling close().  |
| IQW (IQIQIQ)	| .iqw	| A file that contains Float32 data in a binary format ( values are stored in interleaved format, starting with the first I value ). The file does not contain any additional header information. The data order has to be changed before readOpen or writeOpen is called. |
| WV (IQIQIQ)	| .wv	| A file that contains INT16 data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in signal generators.|
|IQX (IQIQIQ)	| .iqx	| A file that contains INT16 data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in device IQW.|
|AID (IQIQIQ)	|.aid	|A file that contains I/Q data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in AMMOS project.|
|CSV	|.csv	|A file containing I/Q data in comma-separated values format (CSV). The comma-separator used can either be a semicolon or a comma, depending on the decimal separator used to save floating-point values (either dot or comma). Additional meta data can be saved. For details see class Csv.|
|Matlab v4	|.mat	|A file containing I/Q data in matlab file format v4. Channel related information is stored in matlab variables with names starting with 'ChX_'. 'X' represents the number of the channel with a lower bound of 1, e.g. variable Ch1_ChannelName contains the name of the first channel. The corresponding data is contained in ChX_Data. |
|Matlab v7.3	|.mat	|A file containing I/Q data in matlab file format v7.3. Supportes the same functionality as matlab v4 file format, but requires the Matlab Compiler Runtime (MCR) to be installed on the system.|

## VITA

### VITA 49.2-2017

The ANSI/VITA 49.2 standard, which is part of the VITA Radio Transport (VRT) family of standards, defines a signal/spectrum protocol that expresses spectrum observation, spectrum operations, and capabilities of RF devices. 

## Inspectrum

## WaveTrap

https://github.com/muaddib1984/wavetrap
