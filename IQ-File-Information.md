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

### gr-sigmf_utils

Utilities for working with SigMF and GNU Radio - Jacob Gilbert. 

https://github.com/jacobagilbert/gr-sigmf_utils/blob/main/README.md

### gr-sigmf

An older OOT module for sigmf. This module contains blocks to read from and write to SigMF (the Signal Metadata Format) recordings in GNU Radio.

https://github.com/skysafe/gr-sigmf

## XMidas Blue format files 

BlueFiles are a file format developed for RF and digital signal processing (DSP) data storage. 

### Blue file version information 

- Gold (original, deprecated)
- BLUE 1.0
- BLUE 1.1 (current community standard)
- BLUE 2.0 / Platinum (a stricter variant / branch of BLUE)

(Within BLUE / Platinum, internal subtypes (TYPE = 1999, 2000, 3000, 4000, 5000, 6000))

For more information, see [Blue File Project Notes](Blue-File-1-1-Project-Notes.md).

## SignalHound - Spike software

I/Q data is stored in a .iq file.

XML data is stored in detached .xml file described in the Spike user manual - https://signalhound.com/sigdownloads/Spike/Spike-User-Manual.pdf

For more information, see [Signal Hound Spike IQ Project Notes](Signal-Hound-Spike-IQ-Project-Notes.md).


## Rohde and Schwarz - I/Q Data File Format (iq-tar)
 
I/Q data is packed in a file with the extension `.iq.tar`. An iq-tar file contains I/Q data in binary format together with meta information that describes the nature and the source of data, e.g. the sample rate. The objective of the iq-tar file format is to separate I/Q data from the meta information while still having both inside one file. In addition, the
 file format allows you to preview the I/Q data in a web browser, and allows you to include user-specific data.

https://www.rohde-schwarz.com/us/applications/converting-r-s-i-q-data-files-application-note_56280-35531.html

The user manual of the IQ Data Recorder has additional information on R&S IQ file formats.

https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_common_library/dl_manuals/dl_user_manual/IQR_UserManual_en_12.pdf

*Includes Metadata: Yes*

For more information, see [Rohde and Schwarz Project Notes](Rohde-Schwarz-Project-Notes.md).

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

### Inspectrum with SigMF Files

Blog Post describing setting up Inspectrum with SigMF Files

https://www.jjhorton.co.uk/posts/inspectrumsigmf/

### Sox - Convert IQ to WAV files

Blog Post describing using Sox to convert IQ to WAV files

https://www.pe0sat.vgnet.nl/sdr/sdr-software/using-iq-files/

## References and background information

### IQ Files and SigMF

https://pysdr.org/content/iq_files.html

### GNU Radio IQ Complex Tutorial

https://wiki.gnuradio.org/index.php/IQ_Complex_Tutorial

### SigMF - Talks

Signal Metadata Format (SigMF) Workshop (January 2022)

https://www.youtube.com/watch?v=AVdnP-0uBkE

libsigmf: Human Tools for Extra-Terrestrial and AI Radios - FOSDEM

https://www.youtube.com/watch?v=gXZQY4okDPw&t=54s

Marc Lichtman - SigMF update GRCon24

https://www.youtube.com/watch?v=NiUy6Gnka3w

### SigMF - Discord

https://discord.com/channels/1063315697498853498/1063315698169937992

### PEØSAT IQ Data Explained

https://www.pe0sat.vgnet.nl/sdr/iq-data-explained/

## IQ File Downloads

### IQ Engine

https://iqengine.org/

### SDRAngel

https://www.sdrangel.org/iq-files/

### SDRPlay iq-demo files

https://www.sdrplay.com/iq-demo-files/

*Page Updated - November 14 2025*
