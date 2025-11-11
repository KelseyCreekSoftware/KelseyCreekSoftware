# Rohde and Schwarz Converter Project Information
*Updated November 10, 2025*

## Rohde & Schwarz "example files"

I/Q Waveform File Conversion for Use with Precise Broadcast Signal Generators includes the file R&S_(R)_PR100_StreamExample_V100.riq which was captured using a R&S specan

https://www.rohde-schwarz.com/sg/applications/i-q-waveform-file-conversion-for-use-with-precise-broadcast-signal-generators-application-note_56280-15603.html

## Rohde and Schwarz I/Q Data Import Export library (daiex)

Daiex is a cross-platform C++ library that provides functions to import and export numeric I/Q data to or from various file formats. The library provides standardized read and write functions that encapsulate all file operations. The following file formats are supported:

|File format| file extension | comment|
| --- | --- |:------------------------------|
| iq-tar|	.iq.tar | An iq-tar file contains I/Q data in binary format together with Metadata that describes the nature and the source of data, e.g. sample rate. The objective of the iq-tar file format is to separate I/Q data from the Metadata while still having both in one file. |
|IQW (IIIQQQ) |	.iqw |	A file that contains Float32 data in a binary format ( first all I values are stored, followed by all Q values ). The file does not contain any additional header information. Note that I and Q data are first buffered to temporary files and are merged when calling close().  |
| IQW (IQIQIQ)	| .iqw	| A file that contains Float32 data in a binary format ( values are stored in interleaved format, starting with the first I value ). The file does not contain any additional header information. The data order has to be changed before readOpen or writeOpen is called. |
| WV (IQIQIQ)	| .wv	| A file that contains INT16 data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in signal generators.|
|IQX (IQIQIQ)	| .iqx	| A file that contains INT16 data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in device IQW.|
|AID (IQIQIQ)	|.aid	|A file that contains I/Q data in a binary format ( values are stored in interleaved format, starting with the first I value ). This format is used in AMMOS project.|
|CSV	|.csv	|A file containing I/Q data in comma-separated values format (CSV). The comma-separator used can either be a semicolon or a comma, depending on the decimal separator used to save floating-point values (either dot or comma). Additional Metadata can be saved. For details see class Csv.|
|Matlab v4	|.mat	|A file containing I/Q data in matlab file format v4. Channel related information is stored in matlab variables with names starting with 'ChX_'. 'X' represents the number of the channel with a lower bound of 1, e.g. variable Ch1_ChannelName contains the name of the first channel. The corresponding data is contained in ChX_Data. |
|Matlab v7.3	|.mat	|A file containing I/Q data in matlab file format v7.3. It supports the same functionality as matlab v4 file format, but requires the Matlab Compiler Runtime (MCR) to be installed on the system.|

https://github.com/Rohde-Schwarz/daiex

## aaronia support for IQ TAR

https://v6-forum.aaronia.de/forum/topic/file-source-block/




