# RF Baseband IQ File Format Information

This document summarizes key formats, standards, and tools related to IQ file handling and metadata. These formats can be evaluated and stack ranked for possible import into SigMF.

## SigMF 

SigMF specifies a way to describe sets of recorded digital signal samples with metadata written in JSON. SigMF can be used to describe general information about a collection of samples, the characteristics of the system that generated the samples, features of signals themselves, and the relationship between different recordings.

*Includes Metadata: Yes*

### SigMF Specification Version v1.2.5

https://sigmf.org/

### SigMF Python library

SigMF is a Python library for working with radio recordings in .sigmf format according to the SigMF standard. It offers a simple and intuitive API for Python developers.

https://sigmf.readthedocs.io/en/latest/index.html#

### libsigmf 

https://github.com/deepsig/libsigmf

### gr-sigmf

An older OOT module for sigmf. This module contains blocks to read from and write to SigMF (the Signal Metadata Format) recordings in GNU Radio.

https://github.com/skysafe/gr-sigmf

## RedWing Blue format files 

BlueFiles are a proprietary file format developed by RedWing Technologies and used primarily by Signal Processing Workstation (SPW) and similar tools for RF and digital signal processing (DSP) data storage.

This MATLAB class is a utility to progressively read through BLUE format files.

https://github.com/Geontech/XMidasBlueReader/

REDHAWK is a software-defined radio (SDR) framework designed to support the development, deployment, and management of real-time software radio applications.

It includes libaries such as blueFileLib.

https://github.com/RedhawkSDR/blueFileLib/blob/develop-2.0/cpp/src/HeaderControlBlock.cc

## Rohde and Schwarz - I/Q Data File Format (iq-tar)
 
 I/Q data is packed in a file with the extension `.iq.tar`. An iq-tar file contains I/Q data in binary format together with meta information that describes the nature and the
 source of data, e.g. the sample rate. The objective of the iq-tar file format is to separate I/Q data from the meta information while still having both inside one file. In addition, the
 file format allows you to preview the I/Q data in a web browser, and allows you to include user-specific data.

https://www.rohde-schwarz.com/us/applications/converting-r-s-i-q-data-files-application-note_56280-35531.html

*Includes Metadata: Yes*

## KeySight - Spectrum Analysis IQ File

### IQ Baseband File Formats Used by Keysight Spectrum Analyzers

Keysight instruments (like the MXA, EXA, and PXA series) and software (such as Keysight VSA and 89600 VSA) support several formats for saving IQ baseband data. These formats vary by instrument, software version, and export method.

### Common Keysight IQ File Formats 

- `.bin`, `.iq` – Raw binary IQ data, often 16-bit signed integers, interleaved I/Q pairs. Typically lacks embedded metadata; parameters like sample rate and center frequency must be known externally.
May be paired with a separate config or XML file.
- `.mat` – MATLAB format used for post-processing and visualization of IQ samples. May include structured variables for IQ data and limited metadata depending on export settings.
- `.csv` – Text-based format with I/Q samples in separate columns. Metadata is rarely embedded but might be inferred from headers or filenames.
- `.tdms` – NI TDMS format occasionally used in Keysight workflows; supports structured metadata and time-series data.
- `.vsa`	VSA Archive	Proprietary container used by 89600 VSA software.	Requires Keysight software to extract
- `.h5` HDF5		Hierarchical format used in some Keysight workflows.	Metadata support.

## MATLAB

For an overview of IQ file encoding and MATLAB, refer to the PySDR topic.

https://pysdr.org/content/iq_files.html#coming-from-matlab

The RF Toolbox is commonly used in MATLAB to work with RF signals

https://www.mathworks.com/help/rf/getting-started.html

There are several MATLAB files distributed with GNU Radio to handle writing to files from MATLAB / Octave. 

https://github.com/gnuradio/gnuradio/tree/master/gr-utils/octave

There are additional functions to handle other data types which are also available in this GitHub repository from Adam Gannon.

https://github.com/adamgann/matlab_utils/tree/master

Additional details on interoperating are covered here.

https://adamgannon.com/2014/11/18/gnuradio_offline_pt1/

MATLAB - comm.BasebandFileReader

https://www.mathworks.com/help/comm/ref/comm.basebandfilereader-system-object.html

## SigMF-NS-NTIA

This Signal Metadata Format SigMF namespace extension describes the National Telecommunications and Information Administration (NTIA)'s open data format for recorded signal datasets.

https://github.com/NTIA/sigmf-ns-ntia/

*Includes Metadata: Yes*

## VITA

### VITA 49.2-2017

The ANSI/VITA 49.2 standard, which is part of the VITA Radio Transport (VRT) family of standards, defines a signal/spectrum protocol that expresses spectrum observation, spectrum operations, and capabilities of RF devices. 

https://www.vita.com/page-1855484

*Includes Metadata: Yes*

## HDF5

ITU-R SM.2117-0 is a data format definition for exchanging stored I/Q data with the intention of spectrum monitoring. Key Bridge Wireless supports the ITU in creating a library for the data format as a contribution to IEEE 1900.8 Working Group. This is an HDF5 read-write Python library for the data format in Recommendation ITU-R SM.2117-0.

https://pypi.org/project/itusm2117/

## Rockwell Collins

Rockwell Collins’ tactical signal receivers offer an optional Data Storage Unit - DSU. The DSU records raw I/Q at selectable sample rates. The data is stored in a proprietary container or a straight binary dump (.iq/.dat).

### Raw Binary Dump Format (.iq / .dat)

The  Raw Binary Dump Format is consecutive I/Q pairs. It is usually 16-bit signed, little-endian by default. The SampleRate and byte-order must be known externally. The file naming often mirrors WIFS naming but with `.iq` suffix.

Filename template: `<MODEL>_<SRATE>_<YYYYMMDD>_<HHMMSS>[_segXX].wfs`

*Includes Metadata: No*

## WAV Audio Files

WAV audio files are used to store audio signals.  The most common WAV audio format is uncompressed audio in the linear pulse-code modulation (LPCM) format. LPCM is also the standard audio coding format for audio CDs, which store two-channel LPCM audio sampled at 44.1 kHz with 16 bits per sample.

https://en.wikipedia.org/wiki/WAV

*Includes Metadata: No*

## GPS Global Navigation Satellite System (GNSS) Software Defined Receiver Metadata Standard

This specification standardizes the metadata associated with GPS GNSS SDR sampled data files and the layout of the binary sample files.

https://sdr.ion.org/

*Includes Metadata: Yes*

## SatNOGS - Signal Conversion

Pending research.

https://community.libre.space/

## Tools

### SigMF Converter

SigMF Converter is an online tool for converting various signal file formats to the SigMF standard. It supports the following formats:

 * `*.vita49` - Vita49 recordings
 
 * `*.wav` (Audio format)

The SigMF Converter outputs:

* `*.sigmf-meta, *.sigmf-data` - SigMF recordings
 
https://iqengine.org/convert

## SigMF Reference Tools

After exporting raw I/Q via MATLAB or Python, use the sigmf CLI (pip install sigmf) to generate accompanying JSON metadata.

`sigmf create --samplerate 1e6 --datatype float32 --center-frequency 100`

### MISP SigMF module

The MISP SigMF module expands a SigMF Recording object into a SigMF Expanded Recording object, and extracts a SigMF archive into a SigMF Recording object.

https://github.com/MISP/misp-modules/blob/main/misp_modules/modules/expansion/sigmf_expand.py

### XMidasBlueReader

This MATLAB class is a utility to progressively read through BLUE format files.

https://github.com/Geontech/XMidasBlueReader/

### Rohde and Schwarz I/Q Data Import Export library (daiex)

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

### Inspectrum

Inspectrum is a tool for analysing captured signals, primarily from software-defined radio receivers.

https://github.com/miek/inspectrum/

Inspectrum supports the following file types:

 * `*.sigmf-meta, *.sigmf-data` - SigMF recordings
 * `*.cf32`, `*.fc32`, `*.cfile` - Complex 32-bit floating point samples (GNU Radio, osmocom_fft)
 * `*.cf64`, `*.fc64` - Complex 64-bit floating point samples
 * `*.cs32`, `*.sc32`, `*.c32` - Complex 32-bit signed integer samples (SDRAngel)
 * `*.cs16`, `*.sc16`, `*.c16` - Complex 16-bit signed integer samples (BladeRF)
 * `*.cs8`, `*.sc8`, `*.c8` - Complex 8-bit signed integer samples (HackRF)
 * `*.cu8`, `*.uc8` - Complex 8-bit unsigned integer samples (RTL-SDR)
 * `*.f32` - Real 32-bit floating point samples
 * `*.f64` - Real 64-bit floating point samples (MATLAB)
 * `*.s16` - Real 16-bit signed integer samples
 * `*.s8` - Real 8-bit signed integer samples
 * `*.u8` - Real 8-bit unsigned integer samples

### Csdr

Csdr, it can convert a real/complex stream from one data format to another, to interface it with other SDR tools and the sound card.

https://github.com/ha7ilm/csdr

### WaveTrap

WAVETRAP is a collection of GNURadio flowgraphs intended to make capturing RF Data in the field fast and simple. 

https://github.com/muaddib1984/wavetrap

### Pushbutton IQ Recorder with descriptive filenames

The Pushbutton IQ Recorder adds descriptive information into the filename that describes the signal.

https://wiki.gnuradio.org/index.php?title=Pushbutton_IQ_Recorder_with_descriptive_filenames

### Artemis

Artemis is a software designed to assist radio frequency (RF) signal identification and storage.

https://www.aresvalley.com/

## References and background information

### IQ Files and SigMF

https://pysdr.org/content/iq_files.html

### GNU Radio IQ Complex Tutorial

https://wiki.gnuradio.org/index.php/IQ_Complex_Tutorial

### PEØSAT IQ Data Explained

https://www.pe0sat.vgnet.nl/sdr/iq-data-explained/

*Page Updated - September 22 2025*
