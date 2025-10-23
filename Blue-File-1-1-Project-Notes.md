# MIDIS Blue File Project Notes

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

- Create python code
- Create unit tests

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

Early idea for blue metadata for hcb, adjunct and extended header

```json
{
  "global": {
    "core:datatype": "cf32",
    "core:sample_rate": 20000000,
    "core:version": "1.0.0",
    "core:description": "Wi-Fi signal capture in the 2.4 GHz ISM band",
    "core:author": "Your Name",
    "core:license": "CC-BY-4.0",
    "core:meta_doi": "10.1234/example.doi",
    "blue:standard": "802.11g",
    "blue:channel": 6,
    "blue:bandwidth": 20e6
  },
  "captures": [
    {
      "core:sample_start": 0,
      "core:frequency": 2437000000,
      "core:datetime": "2025-10-23T12:00:00Z"
    }
  ],
  "annotations": [
    {
      "core:description": "Data frame transmission",
      "blue_hcb:frame_foo": "Data",
      "blue_adj:blah_bar": "Data",
      "blue_eh:lunar_cat": "Data",
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

### BlueFileDump1

```python
#!/usr/bin/env python3

# Blue File Reader with HCB and Extended Header Parsing
# This script reads and parses the HCB (Header Control Block) and
# extended header keywords from a Blue file format.

# Author: Don Marshall (with help from AI!)
# Date: October 23, 2025

import os
import json
import struct
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from astropy.time import Time
from sigmf import SigMFFile # Assuming sigmf library is installed


# --- HCB Layout (fixed fields up to adjunct) ---
HCB_LAYOUT = [
    ("version",   0,   4,  "4s",   "Header version"),
    ("head_rep",  4,   4,  "4s",   "Header representation"),
    ("data_rep",  8,   4,  "4s",   "Data representation"),
    ("detached",  12,  4,  "i",    "Detached header"),
    ("protected", 16,  4,  "i",    "Protected from overwrite"),
    ("pipe",      20,  4,  "i",    "Pipe mode (N/A)"),
    ("ext_start", 24,  4,  "i",    "Extended header start (512-byte blocks)"),
    ("ext_size",  28,  4,  "i",    "Extended header size in bytes"),
    ("data_start",32,  8,  "d",    "Data start in bytes"),
    ("data_size", 40,  8,  "d",    "Data size in bytes"),
    ("type",      48,  4,  "i",    "File type code"),
    ("format",    52,  2,  "2s",   "Data format code"),
    ("flagmask",  54,  2,  "h",    "16-bit flagmask"),
    ("timecode",  56,  8,  "d",    "Time code field"),
    ("inlet",     64,  2,  "h",    "Inlet owner"),
    ("outlets",   66,  2,  "h",    "Number of outlets"),
    ("outmask",   68,  4,  "i",    "Outlet async mask"),
    ("pipeloc",   72,  4,  "i",    "Pipe location"),
    ("pipesize",  76,  4,  "i",    "Pipe size in bytes"),
    ("in_byte",   80,  8,  "d",    "Next input byte"),
    ("out_byte",  88,  8,  "d",    "Next out byte (cumulative)"),
    ("outbytes",  96,  64, "8d",   "Next out byte (each outlet)"),
    ("keylength", 160, 4,  "i",    "Length of keyword string"),
    ("keywords",  164, 92, "92s",  "User defined keyword string"),
    # Adjunct starts at 256
]

# --- Extended header type map ---
TYPE_MAP = {
    "B": (np.int8,    1),
    "I": (np.int16,   2),
    "L": (np.int32,   4),
    "X": (np.int64,   8),
    "F": (np.float32, 4),
    "D": (np.float64, 8),
    "A": (np.dtype("S1"), 1),
}

def read_hcb(path, endian="<"):
    """Read HCB fields and adjunct block."""
    hcb = {}
    with open(path, "rb") as f:
        data = f.read(512)

        # Fixed fields
        for name, offset, size, fmt, desc in HCB_LAYOUT:
            raw = data[offset:offset+size]
            val = struct.unpack(endian+fmt, raw)[0]
            if isinstance(val, bytes):
                val = val.decode("ascii", errors="replace").strip("\x00 ")
            hcb[name] = val

        # Adjunct parsing
        f.seek(256)
        if hcb["type"] == 1000 or 1001:
            hcb["adjunct"] = {
                "xstart": struct.unpack(f"{endian}d", f.read(8))[0],
                "xdelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "xunits": struct.unpack(f"{endian}i", f.read(4))[0],
            }
        elif hcb["type"] == 2000:
            hcb["adjunct"] = {
                "xstart": struct.unpack(f"{endian}d", f.read(8))[0],
                "xdelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "xunits": struct.unpack(f"{endian}i", f.read(4))[0],
                "subsize": struct.unpack(f"{endian}i", f.read(4))[0],
                "ystart": struct.unpack(f"{endian}d", f.read(8))[0],
                "ydelta": struct.unpack(f"{endian}d", f.read(8))[0],
                "yunits": struct.unpack(f"{endian}i", f.read(4))[0],
            }
        else:
            f.seek(256)
            hcb["adjunct_raw"] = f.read(256)

    return hcb

def parse_extended_header(path, hcb, endian="<"):
    """Parse extended header keyword records."""
    if hcb["ext_size"] <= 0:
        return []
    entries = []
    with open(path, "rb") as f:
        f.seek(int(hcb["ext_start"]) * 512)
        bytesRemaining = int(hcb["ext_size"])
        while bytesRemaining > 0:
            lkey = struct.unpack(f"{endian}i", f.read(4))[0]
            lext = struct.unpack(f"{endian}h", f.read(2))[0]
            ltag = struct.unpack(f"{endian}b", f.read(1))[0]
            type_char = f.read(1).decode("ascii", errors="replace")

            dtype, bpe = TYPE_MAP.get(type_char, (np.dtype("S1"), 1))
            val_len = lkey - lext
            val_count = val_len // bpe if bpe else 0

            if type_char == "A":
                raw = f.read(val_len)
                value = raw.rstrip(b"\x00").decode("ascii", errors="replace")
            else:
                value = np.frombuffer(f.read(val_len), dtype=dtype, count=val_count)
                if value.size == 1:
                    value = value[0]
                else:
                    value = value.tolist()

            tag = f.read(ltag).decode("ascii", errors="replace") if ltag > 0 else ""

            total = 4+2+1+1+val_len+ltag
            pad = (8 - (total % 8)) % 8
            if pad: f.read(pad)

            entries.append({
                "tag": tag, "type": type_char, "value": value,
                "lkey": lkey, "lext": lext, "ltag": ltag
            })
            bytesRemaining -= lkey
    return entries


def parse_data_values(path, hcb, endian="<"):
    with open(path, "rb") as f:
        data = f.read(512)
        dtype = data[52:54].decode('utf-8') # eg 'CI' or 'CF'
        print('Data type', dtype)
        endianness = data[8:12].decode('utf-8') # better be 'EEEI'! we'll assume it is from this point on
        print('Endianness', endianness)
        time_interval = np.frombuffer(data[264:272], dtype=np.float64)[0]
        sample_rate = 1/time_interval
        print('Sample rate', sample_rate/1e6, 'MHz')
        data_size = int.from_bytes(data[28:32], byteorder='little')
        print('Data size', data_size)
        extended_header_size = int.from_bytes(data[28:32], byteorder='little')
        filesize = os.path.getsize(path)
        print('File size', filesize)

    # Read in the IQ samples
    if dtype == 'CI':
      samples = np.fromfile(filename, dtype=np.int16, offset=512, count=(filesize-extended_header_size))
      samples = samples[::2] + 1j*samples[1::2] # convert to IQIQIQ...

    if dtype == 'CF':
      # Each complex sample is 8 bytes (2 x float32), so np.complex64 is appropriate
      # samples = np.fromfile(filename, dtype=np.complex64, offset=512, count=(filesize-extended_header_size))
      # No need to reassemble IQ — already complex
      # Each sample is 8 bytes (float64), so compute count
      sample_count = (filesize - extended_header_size) // 8
      samples = np.fromfile(filename, dtype=np.complex64, offset=512, count=sample_count)
 
    # ToDo - how to handle SD type properly?    
    if dtype == 'SD':
      samples = np.fromfile(filename, dtype=np.float64, offset=512, count=(filesize - extended_header_size) // 8)

    # ToDo - dtermine if required - aproach used in Vita49
    # Normalize samples to -1.0 to +1.0 range
    # samples = samples / 32767.0

    # Save out as SigMF data file
    dest_path = filename.rsplit(".",1)[0]
    samples.astype(np.complex64).tofile(f"{dest_path}.sigmf-data")

    # Plot output for debugging
    debug_plot_signal(samples, sample_rate)
    input("Press Enter to continue...")  # Pauses until user presses Enter
    return samples

def blue_to_sigmf(hcb, ext_entries, data_path):
    """
    Build a SigMF metadata dict from parsed BLUE HCB + extended header.
    hcb: dict from read_hcb()
    ext_entries: list of dicts from parse_extended_header()
    data_path: path to the .sigmf-data file
    """
    # Helper to look up extended header values by tag
    def get_tag(tag):
        for e in ext_entries:
            if e["tag"] == tag:
                return e["value"]
        return None

    # --- Global object ---
    datatype_map = {
        "CI": "ci16_le",
        "CF": "cf32_le",
        "RI": "ri16_le",
        "RF": "rf32_le",
    }
    datatype = datatype_map.get(hcb["format"], "ci16_le")

    # Sample rate: prefer adjunct.xdelta, else extended header SAMPLE_RATE
    if "adjunct" in hcb and "xdelta" in hcb["adjunct"]:
        sample_rate = 1.0 / hcb["adjunct"]["xdelta"]
    else:
        sr = get_tag("SAMPLE_RATE")
        sample_rate = float(sr) if sr is not None else None

    global_md = {
        "datatype": datatype,
        "sample_rate": sample_rate,
        "num_channels": int(hcb.get("outlets", 1)),
        "description": hcb.get("keywords", ""),
        "hw": get_tag("SCEPTRE_APPLICATION") or get_tag("SCEPTRE_VER"),
        "author": get_tag("SCEPTRE_TAG1"),
        "version": "1.2.0",
    }

    # --- Captures array ---
    captures = [{
        "sample_start": 0,
        "datetime": get_tag("TIME_EPOCH"),
        "frequency": float(get_tag("ARF_FREQ") or 0.0),
    }]

    # --- Annotations array ---
    annotations = []
    for e in ext_entries:
        if e["tag"] in ("TIME_EPOCH", "ARF_FREQ", "SAMPLE_RATE",
                        "SCEPTRE_APPLICATION", "SCEPTRE_VER", "SCEPTRE_TAG1"):
            continue  # already mapped
        annotations.append({
            "sample_start": 0,
            "comment": f"{e['tag']} ({e['type']})",
            "value": str(e["value"]),
        })

    # --- Final SigMF object ---
    sigmf = {
        "global": global_md,
        "captures": captures,
        "annotations": annotations,
    }

    # Write .sigmf-meta file
    meta_path = os.path.splitext(data_path)[0] + ".sigmf-meta"
    with open(meta_path, "w") as f:
        json.dump(sigmf, f, indent=2)
    print(f"Wrote SigMF metadata to {meta_path}")

    return sigmf



def debug_plot_signal(samples, sample_rate):
    # Plot signal for debugging
    Fs = sample_rate

    # Plot every sample to make sure there's no garbage
    print(len(samples))
    print(filename)
    plt.title("Every Sample >>")
    plt.plot(samples.real[::1])
    plt.show()

    # Detailed plots
    plt.plot(samples.real, ".-")
    plt.plot(samples.imag, ".-")
    plt.legend(["I", "Q"])
    plt.show()
    print(samples)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    n = len(samples)

    [frequencies, psd_db_hz] = calc_power_density_spectrum(Fs=Fs, n=n, iqarray=samples)

    # ax1.figure()
    ax1.plot(frequencies, psd_db_hz)
    ax1.set_title("Power Density spectrum")
    ax1.set_xlabel("Frequency [Hz]")
    ax1.set_ylabel("Power Density [dB/Hz]")
    ax1.grid()

   # ax2.specgram(data.iq_data)
    Pxx, freqs, bins, im = ax2.specgram(samples)
    ax2.set_title("Spectogram")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Frequency [Hz]")
    fig.colorbar(im, ax=ax2).set_label("Power Density [dB/Hz]")

    plt.tight_layout()
    plt.show()

    return

def calc_power_density_spectrum(Fs: float, n: int, iqarray):
    """calculates the power density spectrum of an array of iq data.

    :param float Fs: sampling frequency

    :param int n: length of iq array

    :param _type_ iqarray: iq data in complex array

    :return _type_: frequency bins and logarithmic amplitudes

    """
    window = scipy.signal.windows.hamming(n)
    iq_array = iqarray * window
    if Fs is None:
        Fs = 1

    fft_sig = np.fft.fft(iq_array)
    fft_sig = np.fft.fftshift(fft_sig)
    frequencies = np.fft.fftfreq(n, 1 / Fs)
    frequencies = np.fft.fftshift(frequencies)

    psd = (np.abs(fft_sig) ** 2) / (Fs * n)
    psd_db_hz = 10 * np.log10(psd)

    return [frequencies, psd_db_hz]

def dump_blue_file(path, endian="<"):
    hcb = read_hcb(path, endian)
    print("=== HCB Fields ===")
    for name, _, _, _, desc in HCB_LAYOUT:
        print(f"{name:10s}: {hcb[name]!r}  # {desc}")
    print("\n=== Adjunct ===")
    print(hcb.get("adjunct", hcb.get("adjunct_raw")))

    ext = parse_extended_header(path, hcb, endian)
    print("\n=== Extended Header Keywords ===")
    for e in ext:
        print(f"{e['tag']:20s} [{e['type']}] -> {e['value']}")

    iq_data = parse_data_values(path, hcb, endian)

    # Call the SigMF conversion
    blue_to_sigmf(hcb, ext, f"{path}.sigmf-data")

if __name__ == "__main__":
    filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\SceptretTestFile1.cdif'
    # filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\pulse_cx.tmp' # or cdif
    # filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\sin.tmp' 
    # filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\penny.prm' 
    # filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\keyword_test_file.tmp' # or cdif
    # filename = 'C:\Data1\Ham_Radio\SDR\SigMF-MIDAS-Blue-File-Conversion\PythonDevCode\RustBlueTestFiles\lots_of_keywords.tmp' # or cdif
    dump_blue_file(filename, endian="<")


```


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
