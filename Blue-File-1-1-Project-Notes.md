# MIDIS Blue File Project Notes

*Updated 11/17/2025*

## Overview

For an overview of the Midas Blue file format, refer to this topic in PySDR.

https://pysdr.org/content/iq_files.html#midas-blue-file-format

The 1.1 spec is available here.

https://web.archive.org/web/20150413061156/http://nextmidas.techma.com/nm/nxm/sys/docs/MidasBlueFileFormat.pdf

For a handy html listing of the blue file elements.

- https://sigplot.lgsinnovations.com/html/doc/bluefile.html
- http://nextmidas.techma.com/nm/htdocs/usersguide/BlueFiles.html

## Goal

*Create a python script similar to these to covert Blue 1.1 files to SigMF*

https://github.com/IQEngine/IQEngine/blob/main/api/converters/vita49_to_sigmf/vita49.py

https://github.com/IQEngine/IQEngine/blob/main/tools/sdriq2sigmf/sdriq2sigmf.py

Blue test files are kept here.

https://github.com/sigmf/example_nonsigmf_recordings

SigMF QuickStart is here.

https://github.com/sigmf/sigmf-python/blob/main/docs/source/quickstart.rst

## ToDo

- Validate RF file processing
- Create unit tests
- Use SigMFValidate to validate created meta data
- Consider tests to allow support for python versions, such as 3.7 & 3.13 
- Learn about and test *pip install -sigmf[apps]* 
- Try apps install for WAV converter - https://github.com/sigmf/sigmf-python/tree/main/sigmf/apps

## Code Guidelines

- Use black utility to clean up white space - line length 120

- PEP 8 when it makes sense

## Data mapping

(Assuming IEEE endinaness) 

|Blue |  SigMF  |
|---- |-------- |
| CI  | ci16_le |
| CL  | ci32_le|
| CF  | cf32_le |
| SB  | r8_le|
| SI  | ri16_le|
| SL  | ri32_le|
| SX  | ri64_le|
| SF  | rf32_le|
| SD  | rf64_le|

SigMF data types

```json
    real = "r"
    complex = "c"

    type = floating-point / signed-integer / unsigned-integer
    floating-point = "f32" / "f64"
    signed-integer = "i32" / "i16"
    unsigned-integer = "u32" / "u16"
```

## Blue file version information 

- Gold (original, deprecated)
- BLUE 1.0
- BLUE 1.1 (current community standard)
- BLUE 2.0 / Platinum (a stricter variant / branch of BLUE)

(Within BLUE / Platinum, internal subtypes (TYPE = 1999, 2000, 3000, 4000, 5000, 6000))

## Tools and input streams

### XMidasBlueReader

This MATLAB class is a utility to progressively read through BLUE format files.

https://github.com/Geontech/XMidasBlueReader/

### RUST BlueJay reader

https://docs.rs/crate/bluefile/latest/source/src/bluejay.rs

### Example 2.0 Header from sample file

```
Format-Hex .\2025-06-20_18-35-52_906858500hz.cdif | more
Path:
C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\2025-06-20_18-35-52_906858500hz.cdif

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   42 4C 55 45 45 45 45 49 45 45 45 49 00 00 00 00  BLUEEEEIEEEI....
00000010   00 00 00 00 00 00 00 00 F0 44 00 00 08 08 00 00  ........dD......
00000020   00 00 00 00 00 00 80 40 00 00 00 00 97 3B 61 41  ......?@....?;aA
00000030   E9 03 00 00 43 46 00 00 00 00 00 F1 88 BE E1 41  é...CF.....ñ?_áA
00000040   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000060   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000070   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000080   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000090   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000A0   1D 00 00 00 49 4F 3D 53 63 65 70 74 72 65 00 54  ....IO=Sceptre.T
000000B0   43 5F 50 52 45 43 3D 30 00 56 45 52 3D 32 2E 30  C_PREC=0.VER=2.0
```

#### 1.1 Blue test resource files

https://docs.rs/crate/bluefile/latest/source/resources/test/

```
Format-Hex sin.tmp
Path:
C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\bluefile-main\bluefile-main\resources\test\sin.tmp

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   42 4C 55 45 45 45 45 49 45 45 45 49 00 00 00 00  BLUEEEEIEEEI....
00000010   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000020   00 00 00 00 00 00 80 40 00 00 00 00 00 00 E0 40  ......@......à@
00000030   E8 03 00 00 53 44 00 00 00 00 00 00 00 00 00 00  è...SD..........
00000040   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000060   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000070   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000080   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
00000090   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
000000A0   13 00 00 00 56 45 52 3D 31 2E 31 00 49 4F 3D 58  ....VER=1.1.IO=X
000000B0   2D 4D 69 64 61 73 00 20 20 20 20 20 20 20 20 20  -Midas.
```

Example sigmf - see IQ Engine and http://blpd0.ssl.berkeley.edu/SigMF_data/ for example data sets

A_Sign_in_Space-Medicina.sigmf-meta

```json
{
    "global": {
        "core:datatype": "ci8",
        "core:description": "A Sign in Space: Medicina recording",
        "core:hw": "Medicina Radio Observatory 32 meter antenna (RHCP polarization)",
        "core:recorder": "Medicina VDIF backend",
        "core:sample_rate": 1000000,
        "core:sha512": "67755e41cdb3234c77c825a75791cf5aac9e102329b4c04af320ab48419bc318e6371648a58e4ae9eb1212d24d2d03dc557a17d4771a349cd3e1e74a61c20f5d",
        "core:version": "1.1.1"
    },
    "captures": [
        {
            "core:datetime": "2023-05-24T19:14:59.890000000Z",
            "core:frequency": 8410160000,
            "core:sample_start": 0
        }
    ],
    "annotations": []
}
```

Key fields needed for decoding in GNURadio.

```json
Type

FFT size

center_freq

sample_rate

sample_size 
```

Early idea for blue metadata for hcb, adjunct and extended header.

```json
{
  "global": {
    "core:author": "Blue File Conversion - Unknown Author",
    "core:datatype": "cf32_le",
    "core:description": "IO=Sceptre\u0000TC_PREC=0\u0000VER=2.0",
    "core:hw": "Blue File Conversion - Unknown Hardware",
    "core:core:license": "Blue File Conversion - Unknown License",
    "core:num_channels": 1,
    "core:sample_rate": 1750000.0000000002,
    "core:version": "1.0.0",
    "core:blue_hcb_version": "BLUE",
    "core:blue_hcb_head_rep": "EEEI",
    "core:blue_hcb_data_rep": "EEEI",
    "core:blue_hcb_detached": 0,
    "core:blue_hcb_protected": 0,
    "core:blue_hcb_pipe": 0,
    "core:blue_hcb_ext_start": 17648,
    "core:blue_hcb_ext_size": 2056,
    "core:blue_hcb_data_start": 512.0,
    "core:blue_hcb_data_size": 9034936.0,
    "core:blue_hcb_type": 1001,
    "core:blue_hcb_format": "CF",
    "core:blue_hcb_flagmask": 0,
    "core:blue_hcb_timecode": 2381596552.0,
    "core:blue_hcb_inlet": 0,
    "core:blue_hcb_outlets": 0,
    "core:blue_hcb_outmask": 0,
    "core:blue_hcb_pipeloc": 0,
    "core:blue_hcb_pipesize": 0,
    "core:blue_hcb_in_byte": 0.0,
    "core:blue_hcb_out_byte": 0.0,
    "core:blue_hcb_outbytes": 0.0,
    "core:blue_hcb_keylength": 29,
    "core:blue_hcb_keywords": "IO=Sceptre\u0000TC_PREC=0\u0000VER=2.0",
    "core:blue_adjunct_header_xstart": 0.12667871432857147,
    "core:blue_adjunct_header_xdelta": 5.714285714285714e-07,
    "core:blue_adjunct_header_xunits": 1,
    "core:blue_extended_header_TIME_DELTA": 1e-10,
    "core:blue_extended_header_TIME_EPOCH": "2025-06-20T18:35:52Z",
    "core:blue_extended_header_RF_FREQ": 906858500.0,
    "core:blue_extended_header_ACQETF": 906858500.0,
    "core:blue_extended_header_ACQDATE": "20250620",
    "core:blue_extended_header_ACQTIME": "18:35:52",
    "core:blue_extended_header_SCEPTRE_VER": "5.7.0",
    "core:blue_extended_header_IOVERSION": "Sceptre 5.7.0",
    "core:blue_extended_header_APPLICATION": "Sceptre",
    "core:blue_extended_header_SCEPTRE_BANDWIDTH": 1250000.0,
    "core:blue_extended_header_SBT_BANDWIDTH": 1250000.0,
    "core:blue_extended_header_SBT": 906858500.0,
    "core:blue_extended_header_SBT_FREQ": 906858500.0,
    "core:blue_extended_header_VRF": 906858500.0,
    "core:blue_extended_header_IF": 0.0,
    "core:blue_extended_header_FS": 1750000.0000000002,
    "core:blue_extended_header_SCEPTRE_CHANNEL": 1,
    "core:blue_extended_header_SCEPTRE_CATEGORY": "PRED",
    "core:blue_extended_header_SCEPTRE_STREAM_PATH": "/Input 1/Channel 1",
    "core:blue_extended_header_SCEPTRE_SESSION": "session-file-20251007-181810-221096",
    "core:blue_extended_header_ANTENNA": "NONE",
    "core:blue_extended_header_MISSION": "NONE",
    "core:blue_extended_header_PATH": "NONE",
    "core:blue_extended_header_PATHDELAY": 0.0,
    "core:blue_extended_header_SAMPLE_RATE.UNITS": 3,
    "core:blue_extended_header_OUTPUT_IF.UNITS": 3,
    "core:blue_extended_header_DATA_RF.UNITS": 3,
    "core:blue_extended_header_COL_RF.UNITS": 3,
    "core:blue_extended_header_DATA_BANDWIDTH.UNITS": 3,
    "core:blue_extended_header_DATA_GAIN.UNITS": 35,
    "core:blue_extended_header_EVENT.OFFSET": 0,
    "core:blue_extended_header_EVENT.TIME": 1266787143,
    "core:blue_extended_header_EVENT.TIME.UNITS": 32,
    "core:blue_extended_header_EVENT.DURATION": 0.6453525714571425,
    "core:blue_extended_header_COL_RF": 906858500.0,
    "core:blue_extended_header_COL_RF.EVENT": 0,
    "core:blue_extended_header_DATA_BANDWIDTH": 1250000.0,
    "core:blue_extended_header_DATA_BANDWIDTH.EVENT": 0,
    "core:blue_extended_header_DATA_GAIN": 84.30899810791016,
    "core:blue_extended_header_DATA_GAIN.EVENT": 0,
    "core:blue_extended_header_DATA_INVERSION_FLAG": 0,
    "core:blue_extended_header_DATA_INVERSION_FLAG.EVENT": 0,
    "core:blue_extended_header_DATA_RF": 906858500.0,
    "core:blue_extended_header_DATA_RF.EVENT": 0,
    "core:blue_extended_header_OUTPUT_IF": 0.0,
    "core:blue_extended_header_OUTPUT_IF.EVENT": 0,
    "core:blue_extended_header_SAMPLE_RATE": 1750000.0000000002,
    "core:blue_extended_header_SAMPLE_RATE.EVENT": 0,
    "core:blue_extended_header_TIMETAG.OFFSET": 0,
    "core:blue_extended_header_TIMETAG.TIME": 1266787143,
    "core:blue_extended_header_TIMETAG.TIME.UNITS": 32,
    "core:blue_extended_header_SCEPTRE_MAX_VAL": 654.8604125976562,
    "core:blue_extended_header_SCEPTRE_MIN_VAL": -658.2073974609375,
    "core:blue_extended_header_TUNER_START_ABSC": 2.893764,
    "core:blue_extended_header_PRETUNED_CENTER_FREQ": -2.2250738585072014e-308,
    "core:blue_extended_header_SCEPTRE_TAG1": "LoRa",
    "core:blue_extended_header_SCEPTRE_TAG2": "Meshtastic",
    "core:blue_extended_header_SCEPTRE_TAG3": "SF11",
    "core:blue_extended_header_SCEPTRE_TAG4": "Test",
    "core:blue_extended_header_SCEPTRE_TAG5": "250 kHz",
    "core:blue_extended_header_SCEPTRE_TAG6": "decoded",
    "core:blue_extended_header_SCEPTRE_NOTES": "python3 meshtastic_gnuradio_RX.py -i ffffffff202f6033ef11d2c863080000302abbf12cd6917ba7d4\nTEXT_MESSAGE_APP 33602f20 -> ffffffff Test",
    "core:sha512": "248eccb3caff10d4a8a138d81888ede2c6a323b4a5fe8966aef0b92fcc6ef4c32d400fb6f31f0d86934285763019127fefe6898b0856efe8ff01337c3a9522ef"
  },
  "captures": [
    {
      "core:datetime": "2025-06-20T18:35:52Z",
      "core:frequency": 906858500.0,
      "core:sample_start": 0
    }
  ],
  "annotations": [
    {
      "core:sample_start": 0,
      "core:sample_count": 1129367,
      "core:freq_upper_edge": 908108500.0,
      "core:freq_lower_edge": 906858500.0,
      "core:label": "Sceptere"
    }
  ]
}
```

### Tektronix RSA7100A

Tektronix, RSA7100A spectrum analyzer supports the Midas 2.0 (Platinum BLUE) format, with and without an embedded header.
 
.cdif

This combined file contains header and IF samples (IQ samples for the RSA7100A) in Midas 2.0 (Platinum BLUE) format.

.cdif + .det (or .det12)

This is a separate header (.cdif) file and an IF sample (IQ sample for  RSA7100A)
 

### SignalHound
 
The SignalHound Software just supports the loading of this type of Midas Blue file. 
 
The file extension for these files should be .tmp or .prm. 

Only files that have these characteristics can be loaded properly.  
- Little endian headers and data 
- Cannot be detached 
- Must be 1D complex data (type code 1000) 
- Must have data_format of ‘F’, ‘D’, or ‘I’ 
- Sample rate is retrieved from VariableHeader.x_delta.  


### Spectere

3db labs provides signal processing and analysis software such as Sceptre that saves IQ signals.

https://3db-labs.com/support/#customer-support

### REDHAWK

REDHAWK is a software-defined radio (SDR) framework designed to support the development, deployment, and management of real-time software radio applications. 
It includes libraries such as blueFileLib.

https://github.com/RedhawkSDR/blueFileLib/blob/develop-2.0/cpp/src/HeaderControlBlock.cc

It is possible to integrate REDHAWK with GNURadio. A GNURadio Convention 2017 (GRCon 2017) talk provided information on this integration.

https://github.com/geontech/gnuradio-redhawk

### Blue file field information 

Blue file field information from https://lgsinnovations.github.io/sigfile/bluefile.js.html

ToDo - Determine 1.1 and 2.0 version differences

 | Offset  |  Name      | Size |  Type      | Description                                |
 |:--------|:-----------|:-----|:-----------|:-------------------------------------------|
 |  0      |  version   | 4    |  char[4]   | Header version                             |
 |  4      |  head_rep  | 4    |  char[4]   | Header representation                      |
 |  8      |  data_rep  | 4    |  char[4]   | Data representation                        |
 | 12      |  detached  | 4    |  int_4     | Detached header                            |
 | 16      |  protected | 4    |  int_4     | Protected from overwrite                   |
 | 20      |  pipe      | 4    |  int_4     | Pipe mode (N/A)                            |
 | 24      |  ext_start | 4    |  int_4     | Extended header start, in 512-byte blocks  |
 | 28      |  ext_size  | 4    |  int_4     | Extended header size in bytes              |
 | 32      |  data_start| 8    |  real_8    | Data start in bytes                        |
 | 40      |  data_size | 8    |  real_8    | Data size in bytes                         |
 | 48      |  type      | 4    |  int_4     | File type code                             |
 | 52      |  format    | 2    |  char[2]   | Data format code                           |
 | 54      |  flagmask  | 2    |  int_2     | 16-bit flagmask (1=flagbit)                |
 | 56      |  timecode  | 8    |  real_8    | Time code field                            |
 | 64      |  inlet     | 2    |  int_2     | Inlet owner                                |
 | 66      |  outlets   | 2    |  int_2     | Number of outlets                          |
 | 68      |  outmask   | 4    |  int_4     | Outlet async mask                          |
 | 72      |  pipeloc   | 4    |  int_4     | Pipe location                              |
 | 76      |  pipesize  | 4    |  int_4     | Pipe size in bytes                         |
 | 80      |  in_byte   | 8    |  real_8    | Next input byte                            |
 | 88      |  out_byte  | 8    |  real_8    | Next out byte (cumulative)                 |
 | 96      |  outbytes  | 64   |  real_8[8] | Next out byte (each outlet)                |
 | 160     |  keylength | 4    |  int_4     | Length of keyword string                   |
 | 164     |  keywords  | 92   |  char[92]  | User defined keyword string                |
 | 256     |  Adjunct   | 256  |  char[256] | Type-specific adjunct union (See below for 1000 and 2000 type bluefiles)|
 
 Type-1000 Adjunct
 
 | Offset | Name | Size | Type | Description                      |
 :--------|:-----|:-----|:-----|:---------------------------------|
 |  0     |xstart| 8    |real_8| Abscissa value for first sample  |
 |  8     |xdelta| 8    |real_8| Abscissa interval between samples|
 | 16     |xunits| 4    | int_4| Units for abscissa values        |
 
 Type-2000 Adjunct

 | Offset | Name  | Size | Type | Description                          |
 |:-------|:------|:-----|:-----|:-------------------------------------|
 |  0     |xstart |  8   |real_8| Frame (column) starting value        |
 |  8     |xdelta |  8   |real_8| Increment between samples in frame   |
 | 16     |xunits |  4   |int_4 | Frame (column) units                 |
 | 20     |subsize|  4   |int_4 | Number of data points per frame (row)|
 | 24     |ystart |  8   |real_8| Abscissa (row) start                 |
 | 32     |ydelta |  8   |real_8| Increment between frames             |
 | 36     |yunits |  4   |int_4 | Abscissa (row) unit code             |

## Python code scratch pad

*This code is under development and is not complete*

### blue_file_to_sigmf convertor

Under construction

[blue_file_to_sigmf.py](blue_file_to_sigmf.py)


### ExtendedHeader

```python
    @staticmethod
    def ExtendedHeader(f, hcb):
        """Read the extended header structure."""
        if f is None:
            return []

        # Move read pointer to ext_start * 512
        f.seek(hcb["ext_start"] * 512, os.SEEK_SET)

        ext_header = []
        bytesRemaining = hcb["ext_size"]

        while bytesRemaining > 0:
            # Read fixed fields
            lkey = struct.unpack("<i", f.read(4))[0]   # int32
            lext = struct.unpack("<h", f.read(2))[0]   # int16
            ltag = struct.unpack("<b", f.read(1))[0]   # int8
            type_char = f.read(1).decode("ascii")

            # Value type and size
            valType, valTypeBytes = XMidasBlueReader.FormatType(type_char)
            valCount = (lkey - lext) // valTypeBytes

            # Read values
            if valCount > 0:
                values = np.fromfile(f, dtype=np.dtype(valType), count=valCount)
            else:
                values = np.array([])

            # Read tag
            tag = f.read(ltag).decode("ascii") if ltag > 0 else ""

            key = {
                "lkey": lkey,
                "lext": lext,
                "ltag": ltag,
                "type": type_char,
                "value": values,
                "tag": tag,
            }

            # Align to 8-byte boundary
            total = 4 + 2 + 1 + 1 + (lkey - lext) + ltag
            remainder = (8 - (total % 8)) % 8
            if remainder > 0:
                f.seek(remainder, os.SEEK_CUR)

            bytesRemaining -= lkey
            ext_header.append(key)

        return ext_header
```

### FormatType

```python
    @staticmethod
    def FormatType(formatType):
        """Convert format type character to numpy dtype and size in bytes."""
        mapping = {
            "B": ("int8", 1),
            "I": ("int16", 2),
            "L": ("int32", 4),
            "X": ("int64", 8),
            "F": ("float32", 4),
            "D": ("float64", 8),
            "A": ("S1", 1),  # ASCII char
        }
        if formatType not in mapping:
            raise ValueError(f"Unsupported HCB format type: {formatType}")
        return mapping[formatType]
```

### FormatSize

```python
    @staticmethod
    def FormatSize(formatSize):
        """Convert HCB format size character to number of elements per sample."""
        mapping = {
            "S": 1,
            "C": 2,
            "V": 3,
            "Q": 4,
            "M": (3, 3),
            "T": (4, 4),
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "X": 10,
            "A": 32,
        }
        if formatSize not in mapping:
            raise ValueError(f"Unsupported HCB format size: {formatSize}")
        return mapping[formatSize]
```

### 

```python
# xmidas_blue_reader.py
import os
import struct
import numpy as np
from typing import Any, Dict, List, Tuple, Union

class XMidasBlueReader:
    """
    XMidasBlueReader: Read X-Midas BLUE file (Python port of MATLAB class).
    """

    def __init__(self, bluefile: str, endian: str = "<"):
        """
        Initialize the reader, parse headers, and set the read pointer.

        - bluefile: path to the BLUE file
        - endian: struct unpack endianness, "<" for little-endian, ">" for big-endian
        """
        self.bluefile = bluefile
        self.endian = endian  # used for struct.unpack of HCB and extended header
        self.hcb: Dict[str, Any] = {}
        self.ext_header: List[Dict[str, Any]] = []
        self.dataOffset: int = 0

        with open(self.bluefile, "rb") as f:
            self.hcb = self.HCB(f, self.endian)
            self.ext_header = self.ExtendedHeader(f, self.hcb, self.endian)
            self.resetRead()

    def read(self, numSamples: int = 1) -> Union[np.ndarray, np.complex128]:
        """
        Read numSamples from the current data position.
        Returns:
          - For scalar/real types: array shape (numSamples,)
          - For complex 'C': complex array shape (numSamples,)
          - For vector/matrix sizes: array shape (elementsPerSample, numSamples)
            where elementsPerSample = prod(size) for matrices.
        """
        if numSamples <= 0:
            return np.array([])

        with open(self.bluefile, "rb") as f:
            f.seek(int(self.dataOffset), os.SEEK_SET)

            fmt_size_char = self.hcb["format"][0]  # size code
            fmt_type_char = self.hcb["format"][1]  # type code

            elementsPerSample = self.FormatSize(fmt_size_char)
            elem_count_per_sample = (
                np.prod(elementsPerSample) if isinstance(elementsPerSample, (tuple, list)) else elementsPerSample
            )

            dtype_str, elem_bytes = self.FormatType(fmt_type_char)
            bytesPerSample = int(elem_bytes) * int(elem_count_per_sample)

            bytesRead = int(self.dataOffset - self.hcb["data_start"])
            bytesRemaining = int(self.hcb["data_size"] - bytesRead)

            if bytesPerSample * numSamples > bytesRemaining:
                raise ValueError(
                    f"Requested read longer than remaining: {bytesPerSample * numSamples} vs {bytesRemaining}"
                )

            # Read raw elements, then reshape into [elem_count_per_sample, numSamples] in column-major (Fortran) order
            total_elems = int(elem_count_per_sample) * int(numSamples)

            # Build numpy dtype with endianness for numeric types
            # For string/char ('A' → 'S1'), endianness is irrelevant.
            dtype = np.dtype(dtype_str)
            if dtype_str not in ("S1",) and self.endian in ("<", ">"):
                dtype = dtype.newbyteorder(self.endian)
```
