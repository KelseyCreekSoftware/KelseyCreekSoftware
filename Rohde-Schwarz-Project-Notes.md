# Rohde and Schwarz Converter Project Information

*Updated March 25, 2026*

### DAIEX library as test resources

As part of the DAIEX library as test resources folder contains a number of samples.

https://github.com/Rohde-Schwarz/daiex/tree/master/test/res

## Rohde & Schwarz "example files"

I/Q Waveform File Conversion for Use with Precise Broadcast Signal Generators includes the file R&S_(R)_PR100_StreamExample_V100.riq which was captured using a R&S specan

https://www.rohde-schwarz.com/sg/applications/i-q-waveform-file-conversion-for-use-with-precise-broadcast-signal-generators-application-note_56280-15603.html

### IEEE *DataPort* Crawdad IQ samples

A free IEEE login is requird to access these recordings. For example:

CRAWDAD up/rf_recordings

https://ieee-dataport.org/open-access/crawdad-uprfrecordings

## IQ.TAR File Format Information

See: 

*R&S iq-tar File Format Specification*

https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_common_library/dl_manuals/dl_manual/RS_iq-tar_FileFormatSpecification_en_02.pdf

The iq-tar file format XML schema definition: http://www.rohde-schwarz.com/file/RsIqTar.xsd
(Requires R&S login)


https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_application/application_notes/1ef85/1EF85_3e_Converting_RS_IQ_files.pdf

### I/Q Data File Format (iq-tar)

I/Q data is packed in a file with the extension .iq.tar. An iq-tar file contains I/Q data
in binary format together with meta information that describes the nature and the
source of data, e.g. the sample rate. 

The iq-tar container packs several files into a single .tar archive file. Files in .tar
format can be unpacked using standard archive tools (see http://en.wikipedia.org/wiki/
Comparison_of_file_archivers) available for most operating systems. 

An iq-tar file must contain the following files:

● I/Q parameter XML file, e.g. xyz.xml
Contains meta information about the I/Q data (e.g. sample rate). The filename can
be arbitrarily named, but there must be only one single I/Q parameter XML file inside
an iq-tar file.

● I/Q data binary file, e.g. xyz.complex.float32

A single binary file that contains the binary I/Q data of all channels. 

#### Example XML File #1

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" 
href="open_IqTar_xml_file_in_web_browser.xslt"?>
<RS_IQ_TAR_FileFormat fileFormatVersion="1" 
xsi:noNamespaceSchemaLocation="RsIqTar.xsd" 
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Name>FSV-K10</Name>
  <Comment>Here is a comment</Comment>
  <DateTime>2011-01-24T14:02:49</DateTime>
  <Samples>68751</Samples>
  <Clock unit="Hz">6.5e+006</Clock>
  <Format>complex</Format>
  <DataType>float32</DataType>
  <ScalingFactor unit="V">1</ScalingFactor>
  <NumberOfChannels>1</NumberOfChannels>
<DataFilename>xyz.complex.float32</DataFilename>
<UserData>
  <UserDefinedElement>Example</UserDefinedElement>
</UserData>
  <PreviewData>...</PreviewData>
</RS_IQ_TAR_FileFormat>
```
#### Example XML File #2

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Please open this xml file in the web browser. If the stylesheet 'open_IqTar_xml_file_in_web_browser.xslt' is in the same directory the web browser can nicely display the xml file. -->
<?xml-stylesheet type="text/xsl" href="open_IqTar_xml_file_in_web_browser.xslt"?>
<RS_IQ_TAR_FileFormat fileFormatVersion="1" xsi:noNamespaceSchemaLocation="http://www.rohde-schwarz.com/file/RsIqTar.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Name>---</Name>
  <Comment>TEST</Comment>
  <DateTime>2012-02-23 10:58:58</DateTime>
  <Samples>1000000</Samples>
  <Clock unit="Hz">16000000</Clock>
  <Format>complex</Format>
  <DataType>float32</DataType>
  <ScalingFactor unit="V">1</ScalingFactor>
  <NumberOfChannels>1</NumberOfChannels>
  <DataFilename>File.complex.1ch.float32</DataFilename>
  <UserData></UserData>
</RS_IQ_TAR_FileFormat>
```

### Example File -  MultiChannel_4ch_fromLTE.iq

*NOTE: Data removed from PreviewData node.*

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Please open this xml file in the web browser. If the stylesheet 'open_IqTar_xml_file_in_web_browser.xslt' is in the same directory the web browser can nicely display the xml file. -->
<?xml-stylesheet type="text/xsl" href="open_IqTar_xml_file_in_web_browser.xslt"?>
<RS_IQ_TAR_FileFormat fileFormatVersion="2" xsi:noNamespaceSchemaLocation="http://www.rohde-schwarz.com/file/RsIqTar.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Name>Rohde-Schwarz EUTRA/LTE Analysis Software Version 2.8 Beta 3</Name>
  <Comment>Rohde-Schwarz EUTRA/LTE Analysis Software Version 2.8 Beta 3 Comment</Comment>
  <DateTime>2012-02-13T10:23:04</DateTime>
  <Samples>307200</Samples>
  <Clock unit="Hz">1.536e+007</Clock>
  <Format>complex</Format>
  <DataType>float32</DataType>
  <ScalingFactor unit="V">1</ScalingFactor>
  <NumberOfChannels>4</NumberOfChannels>
  <DataFilename>fritz.complex.4ch.float32</DataFilename>
  <UserData>Rohde-Schwarz EUTRA/LTE Analysis Software Version 2.8 Beta 3 UserData</UserData>
  <PreviewData>
    <ArrayOfChannel length="4">
    <Channel>
      <Name>Channel 1</Name>
      <Comment>Channel 1 of 4</Comment>
      <PowerVsTime>
      <Min>
          <ArrayOfFloat length="256">
            <float>-74</float>      
          </ArrayOfFloat>
        </Max>
      </PowerVsTime>
      <Spectrum>
        <Min>
          <ArrayOfFloat length="256">
        </Min>
      </Spectrum>
      <IQ>
        <Histogram width="64" height="64">
        0000
        </Histogram>
      </IQ>
    </Channel>
    </ArrayOfChannel>
  </PreviewData>
</RS_IQ_TAR_FileFormat>
```

**RS_IQ_TAR_File Format** - The root element of the XML file. 

**Name** - Optional: describes the device or application that created the file.

**Comment** - Optional: contains text that further describes the contents of the file.

**DateTime** - Contains the date and time of type  xs:dateTime

**Samples** - Contains the number of samples of the I/Q data. For multi-channel signals all channels have the same number of samples. One sample can be:
● A complex number represented as a pair of I and Q values
● A complex number represented as a pair of magnitude

**Clock** - Contains the clock frequency in Hz, i.e. the sample rate of the I/Q data.

**Format** - Specifies how the binary data is saved in the I/Q data binary file (see
DataFilename element). Every sample must be in the same format. The format can
be one of the following:

● complex: Complex number in cartesian format, i.e. I and Q values interleaved. I
and Q are unitless

● real: Real number (unitless)

● polar: Complex number in polar format, i.e. magnitude (unitless) and phase
(rad) values interleaved. Requires DataType = float32 or float64

**DataType** - Specifies the binary format used for samples in the I/Q data binary file. The
following data types are allowed:

● int8: 8 bit signed integer data

● int16: 16 bit signed integer data

● int32: 32 bit signed integer data

● float32: 32 bit floating point data (IEEE 754)

● float64: 64 bit floating point data (IEEE 754)

**ScalingFactor** - Optional: describes how the binary data can be transformed into values in the unit
Volt. The binary I/Q data itself has no unit. To get an I/Q sample in the unit Volt the
saved samples have to be multiplied by the value of the ScalingFactor. 
For polar data only the magnitude value has to be multiplied. For multi-channel signals the
ScalingFactor must be applied to all channels.

The attribute unit must be set to "V".

The ScalingFactor must be > 0. If the ScalingFactor element is not defined, a value of 1 V is assumed.

**NumberOfChannels** - Optional: specifies the number of channels, e.g. of a MIMO signal, contained in the
I/Q data binary file. For multi-channels, the I/Q samples of the channels are expected
to be interleaved within the I/Q data file. I

**DataFilename** - Contains the filename of the I/Q data binary file that is part of the iq-tar file.
UserData Optional: contains user, application or device-specific XML data which is not part of
the iq-tar specification. 

**PreviewData** - Optional: contains further XML elements that provide a preview of the I/Q data.

#### Binary Data Interleaving Example: Element order for complex cartesian data (3 channels)

Complex data: I[channel no][time index], Q[channel no][time index]

```txt
I[0][0], Q[0][0],            // Channel 0, Complex sample 0
I[1][0], Q[1][0],            // Channel 1, Complex sample 0
I[2][0], Q[2][0],            // Channel 2, Complex sample 0
I[0][1], Q[0][1],            // Channel 0, Complex sample 1
I[1][1], Q[1][1],            // Channel 1, Complex sample 1
I[2][1], Q[2][1],            // Channel 2, Complex sample 1
I[0][2], Q[0][2],            // Channel 0, Complex sample 2
I[1][2], Q[1][2],            // Channel 1, Complex sample 2
I[2][2], Q[2][2],            // Channel 2, Complex sample 2
```

## Possible mapping

✔ Clock → core:sample_rate

✔ Samples → core:num_samples

✔ DataType=float32 → core:datatype="cf32"

✔ NumberOfChannels → core:num_channels

✔ DateTime → core:datetime (after ISO conversion)

## Rohde and Schwarz I/Q Data Import Export library (daiex)

Daiex is a cross-platform C++ library that provides functions to import and export numeric I/Q data to or from various file formats. 

https://github.com/Rohde-Schwarz/daiex

The library provides standardized read and write functions that encapsulate all file operations. The following file formats are supported:

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

### Other possible file types to be investigated

| Format        | Purpose                | Used By (Typical Instruments/Tools)          | Structure                                   | 
|---------------|-------------------------|-----------------------------------------------|----------------------------------------------|
| RSIQ          | Analysis‑friendly IQ    | R&S VSE (Vector Signal Explorer)              | XML metadata + binary IQ                     | 
| RREC          | Long‑duration recording | FSW, FSV3000, ESW, RTP, R&S Recorder          | Chunked container (header + blocks + index)  |

### Streaming Types

| Format        | Purpose                | Used By (Typical Instruments/Tools)          | Structure                                   | 
|---------------|-------------------------|-----------------------------------------------|----------------------------------------------|
| SCPI Binary   | Streaming (no file)     | Modern analyzers via LAN/SCPI                 | Binary blocks over TCP/USB                   | Used for real‑time streaming. |
| VRT (VITA‑49) | Streaming (no file)     | Some R&S receivers and monitoring systems     | VRT packets (metadata + IQ)                  | Standardized RF format for streaming. |


## Additional Tools 

### RsWaveform

A tool to load, manipulate and save R&S waveform files.

https://github.com/Rohde-Schwarz/RsWaveform

### ArbToolbox

https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_application/application_notes/1gp88/ArbToolbox_UserManual_4.4.pdf

### aaronia support for IQ TAR

https://v6-forum.aaronia.de/forum/topic/file-source-block/

